import { ChildProcess, spawn } from 'child_process'
import { app, ipcMain } from 'electron'
import serve from 'electron-serve'
import * as os from 'os'
import * as path from 'path'
import { createWindow } from './helpers'

const isProd = process.env.NODE_ENV === 'production'
let pythonProcess: ChildProcess | null = null

if (isProd) {
  serve({ directory: 'app' })
} else {
  app.setPath('userData', `${app.getPath('userData')} (development)`)
}

; (async () => {
  await app.whenReady()

  const mainWindow = createWindow('main', {
    width: 1000,
    height: 600,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
    },
  })

  // 動態設置 Python 解釋器的路徑
  const pythonPathDev = os.platform() === 'win32' ? '.venv\\Scripts\\python.exe' : '.venv/bin/python';
  const pythonPath = isProd
    ? path.join(process.resourcesPath, pythonPathDev)
    : pythonPathDev;

  // 啟動 Python 腳本
  pythonProcess = spawn(pythonPath, ['-m', 'yoga_pose_recognition'])

  mainWindow.on('closed', () => {
    // 結束 Python 進程
    if (pythonProcess) {
      pythonProcess.kill()
      pythonProcess = null
    }
    app.quit()
  })

  if (isProd) {
    await mainWindow.loadURL('app://./home')
  } else {
    const port = process.argv[2]
    await mainWindow.loadURL(`http://localhost:${port}/home`)
    // mainWindow.webContents.openDevTools()
  }
})()

app.on('window-all-closed', () => {
  app.quit()
})

ipcMain.on('message', async (event, arg) => {
  event.reply('message', `${arg} World!`)
})
