import "influxdata/influxdb/monitor"
import "influxdata/influxdb/v1"

data =
    from(bucket: "tp2")
        |> range(start: -3s)
        |> filter(fn: (r) => r["_measurement"] == "sHumidity")
        |> filter(fn: (r) => r["_field"] == "humidity")
        |> filter(fn: (r) => r["host"] == "434845c46199")
        |> filter(fn: (r) => r["location"] == "living_room")
        |> aggregateWindow(every: 3s, fn: last, createEmpty: false)

option task = {name: "humidity", every: 3s, offset: 2s}

check = {_check_id: "0c3bd287e7d99000", _check_name: "humidity", _type: "threshold", tags: {}}
crit = (r) => r["humidity"] > 70.0
warn = (r) => r["humidity"] > 60.0
ok = (r) => r["humidity"] < 59.0 and r["humidity"] > 30.0
messageFn = (r) => "Check: ${ r._check_name } is: ${ r._level }"

data
    |> v1["fieldsAsCols"]()
    |> monitor["check"](
        data: check,
        messageFn: messageFn,
        crit: crit,
        warn: warn,
        ok: ok,
    )