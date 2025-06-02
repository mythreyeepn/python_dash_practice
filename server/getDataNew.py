from qpython import qconnection

def send_skew_df_to_kdb(df):
    """
    Sends a DataFrame with columns: isin, skew, crbMode
    to KDB+ and runs the embedded update logic.
    """
    if df.empty:
        return

    # Connect to KDB
    q = qconnection.QConnection(host='localhost', port=5000)
    q.open()

    # Send the DataFrame to KDB as a keyed table with column names matching Q script
    table_data = {
        'isin': df['isin'].astype(str).tolist(),
        'skew': df['skew'].astype(str).tolist(),
        'crbMode': df['crbMode'].astype(str).tolist()
    }

    q.sendSync("df: flip `isin`skew`crbMode!([])", raw=False)  # Create an empty template
    q.set('df', table_data)

    # Q logic from the notepad image
    q_code = r"""
    skewMap: `StrongSell`Sell`Buy`StrongBuy!(1 0.5 -0.5 -1);
    runIdNow: .J `$[string .z.z except "."; "T"];

    res: select time: .z.t, sym: isin, symType: isin, updateTime: .z.t, priority: 0n,
         category: `, buySkew: skewMap[skew], sellSkew: skewMap[skew], runId: runIdNow
         from df;

    res: update buySkew: 0f + buySkew, sellSkew: 0f + sellSkew from res;

    panodb: `$":kdb-panoproxy-credit-nyk-ui-7015";
    (panodb) (`.utils.sendTPUpdateWithoutFlush; `smadUS.tp; `factorSkewConfig; res)
    """

    q.sync(q_code)
    q.close()
