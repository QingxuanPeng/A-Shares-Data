# A-Shares-Data
通过tushare api获取中国沪深股票历史数据
command line：python main.py --data 股票历史数据下载目录 --config 配置文件 --init（操作顺序详细解释）
dependent package：tushare， pandas
操作顺序：1.command line：python main.py --init（第一种操作模式：生成配置文件，生成后配置文件里会有四千多支沪深股票的股票代码和股票名称）
         2.直接run main.py（获取历史股票日线数据并把每只股票的数据单独放入data文件夹）
