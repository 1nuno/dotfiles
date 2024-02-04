import "influxdata/influxdb/monitor"
import "influxdata/influxdb/v1"

data =
    from(bucket: "tp2")
        |> range(start: -3s)
        |> filter(fn: (r) => r["_measurement"] == "sAirQuality")
        |> filter(fn: (r) => r["_field"] == "AIQ")
        |> filter(fn: (r) => r["host"] == "434845c46199")
        |> filter(fn: (r) => r["location"] == "living_room_main_room_corridor")
        |> aggregateWindow(every: 3s, fn: last, createEmpty: false)

option task = {name: "AIQ", every: 3s, offset: 2s}

check = {_check_id: "0c3bd3453b999000", _check_name: "AIQ", _type: "threshold", tags: {}}
crit = (r) => r["AIQ"] > 151.0
warn = (r) => r["AIQ"] > 101.0
info = (r) => r["AIQ"] < 100.0 and r["AIQ"] > 51.0
ok = (r) => r["AIQ"] < 50.0 and r["AIQ"] > 0.0
messageFn = (r) => "Check: ${r._check_name} is: ${r._level}"

data
    |> v1["fieldsAsCols"]()
    |> monitor["check"](
        data: check,
        messageFn: messageFn,
        crit: crit,
        warn: warn,
        info: info,
        ok: ok,
    )