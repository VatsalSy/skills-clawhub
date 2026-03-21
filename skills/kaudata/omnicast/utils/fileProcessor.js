const fs = require('fs');
const pdfParse = require('pdf-parse');
const { extractAndChunkAudio, transcribeChunks } = require('./mediaHelpers');

async function processLocalFile(filePath, mimeType, sessionDir, safeId) {
    let text = "";
    if (mimeType === 'application/pdf') {
        const fileBuffer = await fs.promises.readFile(filePath);
        const pdfData = await pdfParse(fileBuffer);
        text = pdfData.text;
    } else if (mimeType === 'text/plain') {
        text = await fs.promises.readFile(filePath, 'utf8');
    } else if (mimeType === 'video/mp4' || mimeType === 'audio/mp4') {
        const chunkPaths = await extractAndChunkAudio(filePath, sessionDir);
        // Notice we no longer pass the API key down
        text = await transcribeChunks(chunkPaths, safeId);
        chunkPaths.forEach(chunk => { if (fs.existsSync(chunk)) fs.unlinkSync(chunk); });
    } else {
        throw new Error("Unsupported file type uploaded.");
    }
    return text;
}

module.exports = { processLocalFile };
