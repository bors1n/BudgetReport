import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import dates
import seaborn as sns
import numpy as np
from math import ceil

palette_color = sns.light_palette("#77A3A5")
plt.rcParams['font.size'] = '14'


def show_values(axs, orient="v", space=.01):
    """
    Функция для подписей баров на бар плоте.
    """
    def _single(ax):
        if orient == "v":
            for p in ax.patches:
                _x = p.get_x() + p.get_width() / 2
                _y = p.get_y() + p.get_height() + (p.get_height() * 0.01)
                value = '{:.1f}'.format(p.get_height())
                ax.text(_x, _y, value, ha="center")
        elif orient == "h":
            for p in ax.patches:
                _x = p.get_x() + p.get_width() + float(space)
                _y = p.get_y() + p.get_height() - (p.get_height() * 0.5)
                value = '{:.1f}'.format(p.get_width())
                ax.text(_x, _y, value, ha="left")

    if isinstance(axs, np.ndarray):
        for idx, ax in np.ndenumerate(axs):
            _single(ax)
    else:
        _single(axs)


def get_month_data(name_df, month):
    """
    Функция для отбора данных только за прошлый месяц.
    """

    all_data = pd.read_csv(name_df, index_col=[0])
    all_data['Date'] = pd.to_datetime(all_data.Date)
    all_data['Month'] = all_data.Date.dt.month
    all_data['Week'] = all_data.Date.dt.isocalendar().week

    last_month_data = all_data.query('Month == @month - 1')
    last_month_data = last_month_data.assign(Week_in_month=(last_month_data.Date.dt.day/7).apply(lambda x: ceil(x)))

    return last_month_data


def generall_info(df):
    """
    Функция для вывода общей информации за месяц
    """
    full_budget = df.groupby('Type', as_index=False) \
        .agg({'Amount': 'sum'})
    leftover = full_budget.iloc[1, 1] + full_budget.iloc[0, 1]

    start_month = f'Beginning of the month: {full_budget.iloc[1, 1]} rub.'
    month_expenses = f'All expenses: {full_budget.iloc[0, 1]} rub.'
    leftover_string = f'End of the month: {leftover} rub.'

    return start_month, month_expenses, leftover_string


def expenses_by_week(df):
    """
    Функция для поиска расходов по неделям.
    """

    expenses_weeks = df.query('Type == "Expenses"') \
        .groupby('Week_in_month', as_index=False) \
        .agg({'Amount': 'sum'}) \
        .sort_values(by='Week_in_month')

    first_week = f'First week: {expenses_weeks.iloc[0, 1]}'
    second_week = f'Second week: {expenses_weeks.iloc[2, 1]}'
    third_week = f'Third week: {expenses_weeks.iloc[2, 1]}'
    fourth_week = f'Fourth week: {expenses_weeks.iloc[3, 1]}'

    return first_week, second_week, third_week, fourth_week


def top_five_costs(df):
    """
   Функция для определения топ 5 трат за месяц.
   """

    top_five = df.sort_values(by='Amount', ascending=True)[['Category', 'Amount', 'Description']] \
        .reset_index(drop=True).head()

    first_exp = f'{top_five.iloc[0, 2]}: {top_five.iloc[0, 1]}'
    second_exp = f'{top_five.iloc[1, 2]}: {top_five.iloc[1, 1]}'
    third_exp = f'{top_five.iloc[2, 2]}: {top_five.iloc[2, 1]}'
    fourth_exp = f'{top_five.iloc[3, 2]}: {top_five.iloc[3, 1]}'
    fifth_exp = f'{top_five.iloc[4, 2]}: {top_five.iloc[4, 1]}'

    return first_exp, second_exp, third_exp, fourth_exp, fifth_exp


def plot_pai_chart(df, filename, size: tuple = (10, 8)):
    """
    Функция для отрисовки пай чарта.
    """
    expenses_groups = df.query('Type == "Expenses"') \
        .groupby('Category', as_index=False) \
        .agg({'Amount': 'sum'}) \
        .sort_values(by='Amount', ascending=True)

    top_five_expenses = expenses_groups.iloc[:5, :]
    other_expenses = expenses_groups.iloc[5:, :].Amount.sum()
    new_row = {'Category': "Остальные расходы",
               'Amount': other_expenses}
    top_six_expenses = pd.concat([top_five_expenses, pd.DataFrame(new_row, index=[0])]).reset_index(drop=True)

    plt.figure(figsize=size)
    plt.pie(np.abs(top_six_expenses.Amount), labels=top_six_expenses.Category, autopct='%.0f%%', colors=palette_color)
    plt.title('Top 5 spending categories per month', fontsize=16)
    #plt.savefig(f'/Users/bors1n/DataspellProjects/dsProject/budget_report/res/{filename}', dpi=200, bbox_inches='tight')
    plt.savefig(f'/home/admin/projects/budgeting_report/BudgetReport/res/{filename}', dpi=200, bbox_inches='tight')
    plt.close()


def plot_bar_chart(df, filename, size: tuple = (10, 8)):
    """
    Функция для отрисовки бар чарта.
    """
    expenses_groups = df.query('Type == "Expenses"') \
        .groupby('Category', as_index=False) \
        .agg({'Amount': 'sum'}) \
        .sort_values(by='Amount', ascending=True)

    plt.figure(figsize=size)
    ax = sns.barplot(x=np.abs(expenses_groups.Amount), y='Category', data=expenses_groups, palette=palette_color)
    plt.title('All expenses by category', fontsize=18)
    ax.set_xlabel('')
    ax.set_ylabel('')
    show_values(ax, 'h', space=0.05)
    #plt.savefig(f'/Users/bors1n/DataspellProjects/dsProject/budget_report/res/{filename}', dpi=200, bbox_inches='tight')
    plt.savefig(f'/home/admin/projects/budgeting_report/BudgetReport/res/{filename}', dpi=200, bbox_inches='tight')
    plt.close()


def plot_line_chart(df, filename, size: tuple = (10, 8)):
    """
    Функция для отрисовки лайн чарт.
    """
    left_over = df.groupby(['Date', 'Type'], as_index=False) \
        .agg({'Amount': 'sum'}) \
        .pivot_table(index='Date', columns='Type', values='Amount') \
        .reset_index() \
        .fillna(0)

    left_over['CumSum'] = left_over.Income.cumsum()
    left_over['CumSumEx'] = left_over.Expenses.cumsum()
    left_over['Leftover'] = left_over['CumSum'] + left_over['CumSumEx']
    plt.figure(figsize=size)
    ax = sns.lineplot(data=left_over, x='Date', y='Leftover', color='#008080', marker="o")
    plt.xticks(rotation=45)
    ax.set(xticks=left_over.Date.values)
    ax.xaxis.set_major_formatter(dates.DateFormatter("%d-%m-%Y"))
    plt.title('Dynamics of the balance by day', fontsize=18)
    ax.set_xlabel('')
    ax.set_ylabel('')
    #plt.savefig(f'/Users/bors1n/DataspellProjects/dsProject/budget_report/res/{filename}', dpi=200, bbox_inches='tight')
    plt.savefig(f'/home/admin/projects/budgeting_report/BudgetReport/res/{filename}', dpi=200, bbox_inches='tight')
    plt.close()



