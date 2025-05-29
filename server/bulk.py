@app.post("/skews_bulk_update")
async def bulk_update_skews(req: SkewBulkUpdateRequest):
    with pyodbc.connect(connection_string) as conn:
        cursor = conn.cursor()
        now = datetime.utcnow()
        responses = []
        bulk_socket_updates = []
        group_id = str(uuid.uuid4())

        for update in req.updates:
            if update.column not in ["skew", "crb_mode"]:
                continue  # skip invalid columns

            # Check bond exists
            cursor.execute("SELECT 1 FROM skew_bonds WHERE isin = ?", (update.isin,))
            if not cursor.fetchone():
                continue

            # Fetch existing skew and timestamp
            cursor.execute(
                f"SELECT {update.column}, last_updated_at FROM skew_skews WHERE isin = ?",
                (update.isin,)
            )
            result = cursor.fetchone()

            if result:
                old_value, last_updated_at = result
                last_seen = req.client_last_seen_map.get(update.isin) if req.client_last_seen_map else None
                conflict = last_updated_at and last_seen and last_updated_at > last_seen

                # Update
                cursor.execute(
                    f"UPDATE skew_skews SET {update.column} = ?, last_updated_by = ?, last_updated_at = ? WHERE isin = ?",
                    (update.new_value, req.user_id, now, update.isin)
                )
            else:
                old_value = None
                last_updated_at = None
                conflict = False

                skew = update.new_value if update.column == "skew" else None
                crb_mode = update.new_value if update.column == "crb_mode" else None

                cursor.execute(
                    "INSERT INTO skew_skews (isin, skew, crb_mode, last_updated_by, last_updated_at) VALUES (?, ?, ?, ?, ?)",
                    (update.isin, skew, crb_mode, req.user_id, now)
                )

            # Log change
            cursor.execute(
                "INSERT INTO skew_change_log (isin, column_name, old_value, new_value, user_id, timestamp, group_id) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (update.isin, update.column, old_value, update.new_value, req.user_id, now, group_id)
            )

            # Prepare for bulk socket message
            bulk_socket_updates.append({
                "isin": update.isin,
                "column": update.column,
                "new_value": update.new_value,
                "user_id": req.user_id,
                "timestamp": now.isoformat(),
                "conflict": conflict
            })

            responses.append({
                "isin": update.isin,
                "column": update.column,
                "new_value": update.new_value,
                "conflict": conflict
            })

        conn.commit()

        # Send one bulk WebSocket update
        await pubsub_manager.publish(
            channel="trader-skews",
            message={
                "event": "bulk_skew_updated",
                "updates": bulk_socket_updates
            }
        )

        return {"status": "bulk_success", "updated": responses}
