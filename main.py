"""
Example of using OpenDOSM data and plotting
"""

from request_api import get_post
import matplotlib.pyplot as plt

# Example of Passport Issuances by Immigration Department of Malaysia
passport_url = "https://api.data.gov.my/data-catalogue?id=passports"
mypassport = get_post(passport_url, limit=24)

# Example of Monthly Arrivals by Nationality & Sex
arrival_url = "https://api.data.gov.my/data-catalogue?id=arrivals"
myarrival = get_post(arrival_url, limit=24)

if mypassport and myarrival:
    print("Passport data\n", mypassport)
    print("Monthly Arrival data\n", myarrival)
else:
    print('Failed to get response.')

passports = []
arrivals = []
dates = []
for i in range(24):
    passports.append(mypassport[i]["passports"])
    dates.append(mypassport[i]["date"])
    arrivals.append(myarrival[i]["arrivals"])

plt.axvline(x=2.3, ls="--", color="orangered", label="MCO")
plt.plot(range(24), passports, marker="x", color="darkgreen", label="Passports Issuances")
plt.xticks(range(24), dates, rotation=90)
plt.text(3, 150000, "MCO (18 March 2020 - 3 May 2020)", color="firebrick")
plt.title("Passport Issuances in Malaysia 2020-2021")
plt.legend()
plt.show()

plt.axvline(x=2.3, ls="--", color="crimson", label="MCO")
plt.plot(range(24), arrivals, marker="o", color="royalblue", label="Monthly arrivals")
plt.xticks(range(24), dates, rotation=90)
plt.text(3, 2_000_000, "MCO (18 March 2020 - 3 May 2020)", color="crimson")
plt.title("Monthly foreign arrivals in Malaysia 2020-2021")
plt.legend()
plt.show()
