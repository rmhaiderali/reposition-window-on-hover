#!/usr/bin/env node

import { exec } from "child_process"

function getCursorPosAndCtrlKey() {
  return new Promise((resolve) => {
    exec(
      "powershell.exe -Command \"Add-Type -AssemblyName System.Windows.Forms; $cursor = [System.Windows.Forms.Cursor]::Position; $ctrl = if ([System.Windows.Forms.Control]::ModifierKeys -band [System.Windows.Forms.Keys]::Control) { 1 } else { 0 }; Write-Output \\\"$($cursor.X) $($cursor.Y) $ctrl\\\"\"",
      (error, stdout) => {
        if (error) {
          console.error(error)
          process.exit(3)
        }
        const r = stdout.trim().split(" ").map(Number)
        resolve({ x: r[0], y: r[1], ctrl: r[2] })
      }
    )
  })
}

function getScreenSize() {
  return new Promise((resolve) => {
    exec(
      "powershell.exe -Command \"Add-Type -AssemblyName System.Windows.Forms; $screen = [System.Windows.Forms.Screen]::PrimaryScreen; Write-Output \\\"$($screen.WorkingArea.Width) $($screen.WorkingArea.Height)\\\"\"",
      (error, stdout) => {
        if (error) {
          console.error(error)
          process.exit(4)
        }
        const r = stdout.trim().split(" ").map(Number)
        resolve({ w: r[0], h: r[1] })
      }
    )
  })
}

const screenSize = await getScreenSize()

const windowTitle = process.argv[2] || "VLC media player"

const interval = +process.argv[3] || 500

const windowSize = { w: 500, h: 385 }
Object.assign(windowSize, eval("(" + (process.argv[4] || "{}") + ")"))

const windowOffset = { t: 1, l: 8, r: 8, b: 8 }
Object.assign(windowOffset, eval("(" + (process.argv[5] || "{}") + ")"))

let isTop = false

function updatePosition() {
  return new Promise((resolve) => {
    console.log("Setting position to " + (isTop ? "top-left" : "bottom-right"))

    const x = isTop
      ? -windowOffset.l
      : screenSize.w - windowSize.w + windowOffset.r

    const y = isTop
      ? -windowOffset.t
      : screenSize.h - windowSize.h + windowOffset.b

    exec(
      `nircmdc win setsize ititle "${windowTitle}" ${x} ${y} ${windowSize.w} ${windowSize.h}`,
      (error) => {
        if (error.code !== 1073757860) {
          console.error(error)
          process.exit(5)
        }
        resolve()
      }
    )
  })
}

if (interval < 300) {
  console.error("Interval must be at least 300ms")
  process.exit(6)
}

console.log({ interval, windowTitle, windowSize, screenSize, windowOffset })

await updatePosition()

async function updateLoop() {
  const cursorPosAndCtrlKey = await getCursorPosAndCtrlKey()
  if (cursorPosAndCtrlKey.ctrl) return

  if (isTop) {
    if (
      //
      cursorPosAndCtrlKey.x < windowSize.w &&
      cursorPosAndCtrlKey.y < windowSize.h
    ) {
      isTop = false
      await updatePosition()
    }
  } else {
    if (
      cursorPosAndCtrlKey.x > screenSize.w - windowSize.w &&
      cursorPosAndCtrlKey.y > screenSize.h - windowSize.h &&
      cursorPosAndCtrlKey.y < screenSize.h
    ) {
      isTop = true
      await updatePosition()
    }
  }
}

setInterval(updateLoop, interval)
