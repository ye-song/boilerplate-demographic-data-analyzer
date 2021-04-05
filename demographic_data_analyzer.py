import pandas as pd


def calculate_demographic_data(print_data=True):
    # Read data from file
    df = pd.read_csv('adult.data.csv')
    

    # How many of each race are represented in this dataset? This should be a Pandas series with race names as the index labels.
    
    races = df.groupby(['race'])['race'].count()
    race_count = pd.Series(races, index=df['race'].unique())
    
    # What is the average age of men?
    
    average_age_men = df[df['sex'] == 'Male']['age'].mean().round(decimals=1)

    # What is the percentage of people who have a Bachelor's degree?

    number_of_people = len(df)
    number_of_bachelors = len(df[df['education']=='Bachelors'])
    percentage_bachelors = round(number_of_bachelors / number_of_people * 1000) / 10

    # What percentage of people with advanced education (`Bachelors`, `Masters`, or `Doctorate`) make more than 50K?
    # What percentage of people without advanced education make more than 50K?

    # with and without `Bachelors`, `Masters`, or `Doctorate`
    education = df.groupby('education')
    table = education['education'].count()
    total = table['Bachelors'] + table['Masters'] + table['Doctorate']

    higher_education = total
    lower_education = number_of_people - total

    #df[df.index.isin(a_list) & df.a_col.isnull()]
    # percentage with salary >50K
    rich_bachelors = len(df[df['education']=='Bachelors'][df['salary']=='>50K'])
    rich_masters = len(df[df['education']=='Masters'][df['salary']=='>50K'])
    rich_doctorate = len(df[df['education']=='Doctorate'][df['salary']=='>50K'])
    total_highED_rich = rich_bachelors + rich_masters + rich_doctorate

    higher_education_rich = (total_highED_rich / higher_education * 100).round(decimals=1)

    rich = df.loc[df['salary']=='>50K']
    rich_ED = rich.groupby('education')
    table5 = rich_ED['education'].count()
    lowED_rich = sum(table5.drop(['Bachelors', 'Masters', 'Doctorate'], axis='rows'))

    lower_education_rich = (lowED_rich / lower_education * 100).round(decimals=1)

    # What is the minimum number of hours a person works per week (hours-per-week feature)?
    min_work_hours = df['hours-per-week'].min()

    # What percentage of the people who work the minimum number of hours per week have a salary of >50K?
    num_min_workers = df.loc[df['hours-per-week']==min_work_hours]
    min_hours_rich = df.loc[df['hours-per-week']==min_work_hours][df['salary']=='>50K']

    rich_percentage = (len(min_hours_rich) / len(num_min_workers) * 100)

    # What country has the highest percentage of people that earn >50K?

    country = df.groupby('native-country')['native-country'].count()
    country_pop = pd.DataFrame(country, index = df['native-country'].unique())
    country_pop.rename(columns={'native-country': 'population'}, inplace=True)
    country_pop['wealthy'] = df.loc[df['salary']=='>50K'].groupby(['native-country'])['native-country'].count()
    country_pop['%wealthy'] = (country_pop['wealthy'] / country_pop['population'] * 100).round(decimals=1)
    
    
    highest_earning_country = country_pop['%wealthy'].idxmax()
    highest_earning_country_percentage = country_pop['%wealthy'].max()

    # Identify the most popular occupation for those who earn >50K in India.
    table = df.loc[df['salary']=='>50K'][df['native-country']=='India']
    india_occ = table.groupby('occupation')['occupation'].count()
    top_IN_occupation = india_occ.idxmax()

    # DO NOT MODIFY BELOW THIS LINE

    if print_data:
        print("Number of each race:\n", race_count) 
        print("Average age of men:", average_age_men)
        print(f"Percentage with Bachelors degrees: {percentage_bachelors}%")
        print(f"Percentage with higher education that earn >50K: {higher_education_rich}%")
        print(f"Percentage without higher education that earn >50K: {lower_education_rich}%")
        print(f"Min work time: {min_work_hours} hours/week")
        print(f"Percentage of rich among those who work fewest hours: {rich_percentage}%")
        print("Country with highest percentage of rich:", highest_earning_country)
        print(f"Highest percentage of rich people in country: {highest_earning_country_percentage}%")
        print("Top occupations in India:", top_IN_occupation)

    return {
        'race_count': race_count,
        'average_age_men': average_age_men,
        'percentage_bachelors': percentage_bachelors,
        'higher_education_rich': higher_education_rich,
        'lower_education_rich': lower_education_rich,
        'min_work_hours': min_work_hours,
        'rich_percentage': rich_percentage,
        'highest_earning_country': highest_earning_country,
        'highest_earning_country_percentage':
        highest_earning_country_percentage,
        'top_IN_occupation': top_IN_occupation
    }
