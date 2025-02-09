import { createWorker } from 'tesseract.js';
import fs from 'fs';

const worker = await createWorker('tam');

(async () => {
    const { data: { text } } = await worker.recognize('download.jpg');
    console.log(text);
    fs.writeFileSync('output.txt', text);
    await worker.terminate();
})();