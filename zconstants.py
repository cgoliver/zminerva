
"""
where the lowest number is most desirable
"""
OPEN=1
WAITLISTOPEN=2
OVERBOOKED=3
WAITLISTFULL=4
NOWAITLIST=5
NOTACTIVE=6

NOTFOUND=10
UNKNOWN=11

STATUSES={NOTACTIVE:"Not active",
          WAITLISTFULL:"Waitlist is full",
          WAITLISTOPEN:"Waitlist is open",
          OPEN:"Open",
          OVERBOOKED:"Overbooked",
          NOWAITLIST:"Full and no waitlist",
          
          NOTFOUND:"Course not found",
          UNKNOWN:"Course found, unknown status"}