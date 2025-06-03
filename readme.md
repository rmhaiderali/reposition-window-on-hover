# Usage

```bash
npx github:rmhaiderali/reposition-window-on-hover <window-title> <interval> <window-size> <window-offset>
```

Default values

```bash
npx github:rmhaiderali/serve-static-cli "VLC media player" 500 "{}" "{}"
```

| Options       | Discription                                      | Type                                 | Default                        |
| ------------- | ------------------------------------------------ | ------------------------------------ | ------------------------------ |
| window-title  | substring title of window you want to reposition | string                               | "."                            |
| interval      | update loop interval in ms                       | number                               | 3000                           |
| window-size   | size of window                                   | "{ w: int, h: int }"                 | "{ w: 500, h: 385 }"           |
| window-offset | offset of window                                 | "{ t: int, l: int, r: int, b: int }" | "{ t: -1, l: -8, r: 8, b: 8 }" |
