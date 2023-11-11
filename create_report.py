from fpdf import FPDF
import datetime
import calendar
import os

from functions import plot_pai_chart, get_month_data, \
                                    plot_bar_chart, plot_line_chart, \
                                    generall_info, expenses_by_week, \
                                    top_five_costs
WIDTH = 210
HEIGHT = 297

# get data
#name_df = '/Users/bors1n/DataspellProjects/dsProject/budget_report/all_data.csv'
name_df = '/home/admin/projects/budgeting_report/BudgetReport/all_data.csv'

# get date
today = datetime.date.today()
currentMonth = today.month

# get information about last month
df = get_month_data(name_df, currentMonth)
start_month_info, month_expenses_info, leftover_info = generall_info(df)
first_week, second_week, third_week, fourth_week = expenses_by_week(df)
first_cost, second_cost, third_cost, fourth_cost, fifth_cost = top_five_costs(df)

# plotting
plot_pai_chart(df, filename='pie_test.png')
plot_bar_chart(df, filename='bar_test.png', size=(10, 6))
plot_line_chart(df, filename='line_test.png', size=(14, 6))

pdf = FPDF()
pdf.add_page()

# add unicode font
# pdf.add_font('DejaVu', '', 'DejaVuSansCondensed.ttf', uni=True)

# background
#pdf.image('/Users/bors1n/DataspellProjects/dsProject/budget_report/res/My_project-2.png', 0, 0, WIDTH)
pdf.image('/home/admin/projects/budgeting_report/BudgetReport/res/My_project-2.png', 0, 0, WIDTH)

# pai plot
pdf.image('/home/admin/projects/budgeting_report/BudgetReport/res/pie_test.png', 92, 55, 115, 90)
#pdf.image('/Users/bors1n/DataspellProjects/dsProject/budget_report/res/pie_test.png', 92, 55, 115, 90)

# line plot
pdf.image('/home/admin/projects/budgeting_report/BudgetReport/res/pie_test.png', 92, 55, 115, 90)
#pdf.image('/Users/bors1n/DataspellProjects/dsProject/budget_report/res/pie_test.png', 92, 55, 115, 90)

# bar plot
pdf.image('/home/admin/projects/budgeting_report/BudgetReport/res/pie_test.png', 92, 55, 115, 90)
#pdf.image('/Users/bors1n/DataspellProjects/dsProject/budget_report/res/pie_test.png', 92, 55, 115, 90)

# title and info
pdf.set_font('Arial', '', 24)
pdf.ln(65)
pdf.write(5, f'{calendar.month_name[currentMonth - 1]}.')
pdf.ln(10)
pdf.set_font('Arial', '', 14)
pdf.write(4, start_month_info)
pdf.ln(7)
pdf.write(4, month_expenses_info)
pdf.ln(7)
pdf.write(4, leftover_info)

#expenses by week
pdf.set_font('Arial', '', 14)
pdf.set_xy(x=140, y=155)
pdf.write(5, 'Expenses by week.')
pdf.set_xy(x=140, y=162)
pdf.set_font('Arial', '', 12)
pdf.write(5, f'{first_week}')
pdf.set_xy(x=140, y=168)
pdf.write(4, f'{second_week}')
pdf.set_xy(x=140, y=174)
pdf.write(4, f'{third_week}')
pdf.set_xy(x=140, y=180)
pdf.write(4, f'{fourth_week}')


#top five costs
pdf.set_xy(x=2, y=225)
pdf.set_font('Arial', '', 14)
pdf.write(5, 'Top five costs.')
pdf.set_xy(x=2, y=232)
pdf.set_font('Arial', '', 12)
pdf.write(4, f'{first_cost}')
pdf.set_xy(x=2, y=238)
pdf.write(4, f'{second_cost}')
pdf.set_xy(x=2, y=244)
pdf.write(4, f'{third_cost}')
pdf.set_xy(x=2, y=250)
pdf.write(4, f'{fourth_cost}')
pdf.set_xy(x=2, y=256)
pdf.write(4, f'{fifth_cost}')

pdf.output('/home/admin/projects/budgeting_report/BudgetReport/report.pdf', 'F')
#pdf.output('/Users/bors1n/DataspellProjects/dsProject/budget_report/report.pdf', 'F')
#print('Done')


#%%
