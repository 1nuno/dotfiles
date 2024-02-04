import "influxdata/influxdb/monitor"
import "influxdata/influxdb/v1"

data =
    from(bucket: "tp2")
        |> range(start: -3s)
        |> filter(fn: (r) => r["_measurement"] == "sTemperature")
        |> filter(fn: (r) => r["_field"] == "temp2")
        |> filter(fn: (r) => r["host"] == "434845c46199")
        |> filter(fn: (r) => r["location"] == "main_room")
        |> aggregateWindow(every: 3s, fn: last, createEmpty: false)

option task = {name: "temp2", every: 3s, offset: 2s}

check = {_check_id: "0c3bd04b08999000", _check_name: "temp2", _type: "threshold", tags: {}}
crit = (r) => r["temp2"] < 10.0 or r["temp2"] > 35.0
messageFn = (r) => "Check: ${ r._check_name } is: ${ r._level }"

data |> v1["fieldsAsCols"]() |> monitor["check"](data: check, messageFn: messageFn, crit: crit)
