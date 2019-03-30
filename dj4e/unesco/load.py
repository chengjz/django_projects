
import csv  # https://docs.python.org/3/library/csv.html

# python3 manage.py shell < many/load.py

from unesco.models import Site, Iso, Category, States, Region

fhand = open('unesco/load.csv')
reader = csv.reader(fhand)

Site.objects.all().delete()
Iso.objects.all().delete()
Category.objects.all().delete()
States.objects.all().delete()
Region.objects.all().delete()


# Format
# jane@tsugi.org,I,Python
# ed@tsugi.org,L,Python

k = 0;
for row in reader:
    print(row[0])
    k = k + 1
    if k == 1 : continue

    try:
        i = Iso.objects.get(name=row[10])
    except:
        print("Inserting person",row[10])
        i = Iso(name=row[10])
        i.save()

    try:
        c = Category.objects.get(name=row[7])
    except:
        print("Inserting course",row[7])
        c = Category(name=row[7])
        c.save()

    try:
        r = Region.objects.get(name=row[9])
    except:
        print("Inserting course",row[9])
        r = Region(name=row[9])
        r.save()

    try:
        s = States.objects.get(name=row[8])
    except:
        print("Inserting course",row[8])
        s = States(name=row[8])
        s.save()

    # try:
    #     name = chr(row[0])
    # except:
    #     name = None

    # try:
    #     description = chr(row[1])
    # except:
    #     description = None

    # try:
    #     justification = chr(row[2])
    # except:
    #     justification = None

    try:
        year = int(row[3])
    except:
        year = None

    # try:
    #     longitude = float(row[4])
    # except:
    #     longitude = None

    # try:
    #     latitude = float(row[5])
    # except:
    #     latitude = None

    # try:
    #     area_hectares = float(row[6])
    # except:
    #     area_hectares = None



    site = Site(name=row[0], description=row[1], justification=row[2], year=year, longitude=row[4], latitude=row[5], area_hectares=row[6],category=c, states=s, region=r, iso=i)
    site.save()


