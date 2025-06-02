from qpython import qconnection
import pandas as pd

def send_df_to_kdb(df: pd.DataFrame):
    # Connect to KDB
    q = qconnection.QConnection(host='localhost', port=5000)
    q.open()

    # Send DataFrame to KDB as variable `df`
    q.sendSync("df: ([] isin:`symbol$(); skew:`symbol$(); updatetime:`timestamp$(); user:`symbol$())")  # Ensure `df` is initialized
    q.sendSync("df: enlist each (" + ",".join([
        "`" + str(row['isin']),
        "`" + str(row['skew']),
        str(row['updatetime']),
        "`" + str(row['user'])
    ]) + ")" for _, row in df.iterrows())

    # Define and execute the Q logic
    q_code = r"""
    skewMap: `StrongSell`Sell`Buy`StrongBuy!(0.5 -0.5 0 1);
    runIdNow: .J `$[string .z.z except "."; "T"];

    res: select time: .z.t, sym: isin, symType: isin, updateTime: .z.t, priority: 0n, category: `, 
              buySkew: skewMap[skew], sellSkew: skewMap[skew], runId: runIdNow from df;

    res: update buySkew: 0f + buySkew, sellSkew: 0f + sellSkew from res;

    panodb: `$":kdb-panoproxy-credit-nyk-ui-7015";
    (panodb) (`.utils.sendTPUpdateWithoutFlush; `smadUS.tp; `factorSkewConfig; res)
    """

    q.sync(q_code)
    q.close()
