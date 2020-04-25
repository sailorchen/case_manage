import xlrd



data = xlrd.open_workbook('test.xls')
table = data.sheet_by_name('Sheet1')

def check_data(table=None):
	module_list=['login','登录']
	version_list = ['小程序']
	rows = table.nrows
	cols = table.ncols
	for row in range(1,rows):
		if not table.cell_value(row,0):
			print ('用例名称不能为空')
			return False
		if not table.cell_value(row,1) in ('UI','Function','Perfermance'):
			print ('用例类型不正确')
			return False
		if not table.cell_value(row,2) in ('SMOKING','LEVEL0','LEVEL1','LEVEL2'):
			print ('用例等级不正确')
			return False
		if not table.cell_value(row,4):
			print ('用例步骤不能为空')
			return False
		if not table.cell_value(row,7):
			print ('期望结果不能为空')
			return False
		if not table.cell_value(row,5):
			print ('模块不能为空')
			return False
		if not table.cell_value(row,6):
			print ('版本不能为空')
			return False
		if not table.cell_value(row,9):
			print ('测试负责人不能为空')
			return False
		return True

if check_data(table):
	print ('导入成功')
else:
	print ('导入失败')