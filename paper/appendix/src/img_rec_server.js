const express = require('express');
const multer = require('multer');
const { PythonShell } = require('python-shell');
const bodyParser = require('body-parser'); 
const fs = require('fs');

const app = express();
const hostname = 'michael.info.kanazawa-it.ac.jp';
const port = 3000;

const winston = require('winston');

const logger = winston.createLogger({
  level: 'info',
  format: winston.format.json(),
  defaultMeta: { service: 'user-service' },
  transports: [
    new winston.transports.File({ filename: 'error.log', level: 'error' }),
    new winston.transports.File({ filename: 'combined.log' }),
    new winston.transports.Console()
  ]
});


//logger.error('Error message');


const multerStorage = multer.diskStorage({
destination (req, file, cb) {
cb(null, './uploads');
},
filename (req, file, cb) {
cb(null, Date.now() +file.originalname);
//cb(null, Date.now() +'.'+ file.originalname.split('.').pop(1));
}
});
const upload = multer({ storage: multerStorage });
/*const upload = multer({ 
  storage: multer.diskStorage({
  dest: '/uploads',
  filename: (file, filename) => {
    const extension = file.originalname;
    ;
    return `${filename}-${Date.now()}.${extension}`;
    },
  }),
});
*/


app.use(bodyParser.raw({ type: 'image/png' }));
app.use(express.static('/home/lab2015/tamura/srv/webserver'));

//分類ページからのアクセスを処理する
app.post('/img', upload.single('image'), (req, res) => {
  logger.info('The file has been uploaded to '+req.file.path);
  const options = {
    mode: 'text',
    pythonOptions: ['-u'],
    scriptPath: './python',
    args: [req.file.path]
  };

  //スクリプトを読み込んで実行
  
  PythonShell.run('classify.py', options)
    .then((results) => {
    
    //res.send(results[0]);
    res.send(results[2]);

    logger.info('The result has been received');
    logger.info('image classification success')
    })
    .catch((err) =>{
      logger.error(err);
    });
});

//識別ページからのアクセスを処理する
app.post('/identify', upload.single('image'), (req, res) => {
  logger.info('The file has been uploaded to '+req.file.path);
  const options = {
    mode: 'text',
    pythonOptions: ['-u'],
    scriptPath: './python',
    args: [req.file.path]
  };

  //スクリプトを読み込んで実行
  PythonShell.run('identify.py', options)
    .then((results) => {
    logger.info('The result has beed saved in '+ results[3]);
    
    //res.send(results[2]);
    res.send(results[3]);
    logger.info('image identification success');
    
    })
    .catch((err) =>{
      logger.error(err);
    });
});

//動画のページからのアップロード
app.post('/video', upload.single('file'), (req, res) => {
  logger.info('The file has been uploaded to '+req.file.path);
  const options = {
    mode: 'text',
    pythonOptions: ['-u'],
    scriptPath: './python',
    args: [req.file.path]
  };

  //スクリプトを読み込んで実行
  PythonShell.run('video.py', options)
    .then((results) => {
    logger.info('The result has beed saved in'+ results[results.length-1]);
    /*
    let length = results.length;
    for (let i = 0; i < length; i++){
      let element = results[i];
      console.log(results[i]);
    }*/
    //console.log('results[len]: %j', results[results.length-1]);
    
    
    //res.send(results[2]);
    res.send(results[results.length-1]);
    logger.info('video identification success');
    })
    .catch((err) =>{
      logger.error(err);
    });
});

app.listen(3000, () => {
  logger.info(`Server is running at http://${hostname}:${port}`);
  //console.log(`Server is running at http://${hostname}:${port}`);
});
