from analysis import *

calculate_and_write_pnl(db_path="all_data.db", output_path="trade_pnls.txt")
analyze_pnls_by_company(pnl_file_path="trade_pnls.txt", output_path="company_pnl_summary.txt")