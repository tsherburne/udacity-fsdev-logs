#!/usr/bin/env python2


# Logs Analysis Reports

import psycopg2

db = psycopg2.connect(
                    database="news",
                    user="postgres",
                    password="postgres1234")
c = db.cursor()

# Report #1 - What are the most popular three articles of all time?
c.execute("select a.title, count(*) as num from log l, articles a \
    where l.path = concat('/article/', a.slug) and l.status = '200 OK' \
    and l.path != '/' group by a.title order by num desc limit 3")

results = c.fetchall()

print("What are the most popular three articles of all time")
print("====================================================")

for report_item in results:
    print("\"" + report_item[0] + "\" -- " + str(report_item[1]) + " views")

print("\n\n")

# Report #2 - Who are the most popular article authors of all time?
c.execute("select name, sum(num) from \
    (select au.name, a.title, count(*) as num from log l, \
        articles a, authors au \
        where l.path = concat('/article/', a.slug) and a.author = au.id and \
        l.status = '200 OK' and l.path != '/' \
        group by au.name, a.title order by num desc) as popular \
    group by name order by sum desc")

results = c.fetchall()
print("Report #2 - Most Popular Authors of All Time")
print("============================================")

for report_item in results:
    print(report_item[0] + " -- " + str(report_item[1]) + " views")

print("\n\n")

# Report #3 - On which days did more than 1% of requests lead to errors?
c.execute("select l.date, l.total, e.total, \
  round((cast(e.total as numeric) / cast(l.total as numeric) * 100), 2) \
  as percent from daily_logs l, daily_errors e where l.date = e.date and \
  round((cast(e.total as numeric) / cast(l.total as numeric) * 100), 2) > 1.0 \
  order by percent desc")

results = c.fetchall()
print("Report #3 - Which days did more than 1% of requests lead to errors?")
print("===================================================================")

for report_item in results:
    print(
        report_item[0].strftime('%b %d %Y') +
        " -- " + str(report_item[3]) + "% errors")

db.close()
