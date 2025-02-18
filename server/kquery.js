import { useState, useRef } from 'react';
import { useWebSocket } from 'react-use-websocket';

export default function useQueryKDB(url: string) {
  const [error, setError] = useState<any>(null);
  const [data, setData] = useState<any>(null);
  const pendingRequests = useRef<Map<string, (value: any) => void>>(new Map()); // Store query promises

  const { sendMessage } = useWebSocket(url, {
    share: false,
    onOpen: () => console.log('useQueryKDB WebSocket opened'),
    onMessage: (event) => {
      const response = JSON.parse(event.data);
      console.log('Received KDB response:', response);

      // Assuming the response includes some form of query matching (e.g., query string or timestamp)
      if (response.query && pendingRequests.current.has(response.query)) {
        // Match the response to the stored query using `query`
        pendingRequests.current.get(response.query)?.(response.result); // Resolve the promise
        pendingRequests.current.delete(response.query);
      } else {
        setData(response); // Fallback if no matching query found
      }
    },
    onError: (event) => {
      const msg = `Error querying: ${url}`;
      setError(msg);
      console.error(msg);
    },
  });

  const sendQuery = (query: string): Promise<any> => {
    return new Promise((resolve, reject) => {
      const queryId = `query-${Date.now()}`; // Unique ID for tracking
      const queryObject = { queryId, query }; // Add `queryId` to the query object

      // Store the resolver function so we can resolve when the response arrives
      pendingRequests.current.set(queryId, resolve);

      try {
        sendMessage(JSON.stringify(queryObject)); // Send query with ID
      } catch (err) {
        pendingRequests.current.delete(queryId); // Cleanup on failure
        reject(err);
      }
    });
  };

  return [sendQuery, data, error] as const;
}
