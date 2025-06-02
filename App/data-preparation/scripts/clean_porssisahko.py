import pandas as pd
import datetime
import sys

def clean_data(filename):
    # Read the CSV file
    df = pd.read_csv(filename, sep=",", encoding="utf-8")

    # Extract times and prices
    times = df["Aika"].tolist()
    prices = df[df.columns[1]].tolist()

    # Convert prices to float, handle errors by setting to average of adjacent values
    for i in range(len(prices)):
        try:
            #prices[i] = float(prices[i].replace(",", "."))
            prices[i] = float(prices[i])
        except ValueError:
            print(f"Invalid price at index {i}: {prices[i]}")
            if i == 0:
                prices[i] = prices[i + 1]
            elif i == len(prices) - 1:
                prices[i] = prices[i - 1]
            else:
                prices[i] = (prices[i - 1] + prices[i + 1]) / 2

    # Extract year, month, day, hour, and weekday
    years = []
    months = []
    days = []
    hours = []
    weekdays = []
    dates = []
    datetimes = []

    for line in times:
        #datetimes.append(line)
        date = line.split(" ")[0]
        time = line.split(" ")[1]
        year, month, day = date.split("/")
        hour = time.split(":")[0]
        
        # datetime as "YYYY-MM-DD HH:00:00",always beginning hours
        datetime_str = f"{year}-{month.zfill(2)}-{day.zfill(2)} {hour.zfill(2)}:00:00"
        datetimes.append(datetime_str)

        dates.append(date)
        years.append(int(year))
        months.append(int(month))
        days.append(int(day))
        hours.append(int(hour))
        weekday = datetime.datetime(int(year), int(month), int(day)).weekday()
        weekdays.append(weekday)        

    # Create a new DataFrame
    df2 = pd.DataFrame({
        "datetime": datetimes,
        "date": dates,
        "year": years,
        "month": months,
        "day": days,
        "hour": hours,
        "weekday": weekdays,
        "price": prices
    })

    # Save the cleaned data to a new CSV file
    output_file = filename.replace(".csv", "_cleaned.csv")
    df2.to_csv(output_file, index=False, sep=";")
    print(f"Cleaned data saved to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python clean_data.py <filename>")
        sys.exit(1)

    input_file = sys.argv[1]
    clean_data(input_file)