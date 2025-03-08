import { createWorker } from 'tesseract.js';
import fs from 'fs';

const worker = await createWorker('eng');

(async () => {
    const { data: { text } } = await worker.recognize('New folder\\WhatsApp Image 2025-03-07 at 15.51.53_b859b5ce.jpg');
    console.log(text);
    fs.writeFileSync('output.txt', text);
    await worker.terminate();
})();