# `tpl`: Render templates with data from various sources

You want to fill data into a template file?
```shell
tpl --yaml data.yaml template.file > rendered.file
```

You have everything already set up in your environment and now you just want to
POST it somewhere?
```shell
tpl structure.json | curl -X POST -H "Content-Type: application/json" -d@- httpbin.org/anything
```

## Installation
```shell
make install
```

## Input sources

`tpl` supports multiple sources:
 * YAML files (`--yaml <file>`)
 * JSON files (`--json <file>`)
 * environment variables (`--environment`)

You can specify multiple sources at once, but if a key is present in more than
one then it's value will be taken from the latter source. This can be useful if
you have default values that you want to always be present:
```bash
tpl \
  --yaml defaults.yaml \
  --json <(curl -H "Content-Type: application/json" now.httpbin.org) \
  template.jinja2 > results.html
```
