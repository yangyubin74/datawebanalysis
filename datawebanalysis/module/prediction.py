
import datawebanalysis.module.sqlgen as sql
import pandas as pd

#�̵� ��� ����
def get_average_prediction():
    try:
        # �����ͺ��̽����� ������ ��������
        df = sql.select_common_data()

        # ������ ��ó��
        df['buy_amt'] = df['buy_amt'].astype('int64')
        df['order_dt'] = pd.to_datetime(df['order_dt'])
        df['order_month'] = pd.to_datetime(df['order_dt']).dt.to_period('M')

        # �׷�ȭ �� ��� ����
        filtered_df = df.groupby(['bld_name', 'order_month'], as_index=False)['buy_amt'].sum()
        filtered_df['order_month'] = filtered_df['order_month'].astype(str)

        return filtered_df
    except Exception as e:
        # ���� �α� �߰�
        print(f"Error in get_average_prediction: {e}")
        raise  # ���ܸ� �ٽ� �߻����� ȣ���ڿ��� ����