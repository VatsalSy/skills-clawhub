const express = require('express');
const fs = require('fs');
const path = require('path');
const { GoogleGenAI } = require('@google/genai');
const state = require('../config/state');
const { emitStreamLog } = require('../utils/streamer');

const router = express.Router();

router.post('/draft-script', async (req, res) => {
    const { id, host1 = 'Alex', host2 = 'Sam', targetLanguage = 'English' } = req.body;
    const safeId = state.sanitizeId(id);
    const sessionDir = path.join(state.downloadsDir, safeId);
    const apiKey = process.env.GEMINI_API_KEY;

    if (!apiKey) return res.status(401).json({ error: "Gemini API key is missing in environment." });
    
    const sourceFile = path.join(sessionDir, 'original.txt');
    if (!fs.existsSync(sourceFile)) return res.status(404).json({ error: "Source text not found." });

    try {
        const sourceText = fs.readFileSync(sourceFile, 'utf8');
        const ai = new GoogleGenAI({ apiKey: apiKey });

        emitStreamLog(safeId, { message: `Drafting ${targetLanguage} multi-host script via Gemini...` });

        let finalScript = "";
        let attempt = 1;
        const maxAttempts = 3;
        let success = false;

        while (attempt <= maxAttempts && !success) {
            // If the model fails the first attempt, aggressively command it to cut details
            const urgencyModifier = attempt > 1 
                ? `\n\nCRITICAL WARNING: Your previous draft was TOO LONG. You MUST summarize further and aggressively cut minor details to compress the runtime. The absolute maximum length is 2100 words.` 
                : "";

            const systemPrompt = `You are a professional podcast producer and scriptwriter.
            Convert the following source text into an engaging, conversational podcast script.
            
            CRITICAL GROUNDING RULES:
            1. Rely SOLELY on the provided Source Material. 
            2. DO NOT invent, hallucinate, or infer any external facts, figures, examples, or names not explicitly mentioned in the text.
            3. If the source material is brief, the podcast must be brief. Do not pad the script with outside knowledge or generic filler.
            
            FORMATTING RULES:
            4. Use exactly two hosts: ${host1} (Host 1) and ${host2} (Host 2).
            5. Output language must be ${targetLanguage}.
            6. Format every line EXACTLY like this: "Name: Spoken text here."
            7. Do NOT include sound effects, brackets, or stage directions.
            8. The final script MUST NOT exceed 2100 words.${urgencyModifier}`;

            if (attempt > 1) {
                emitStreamLog(safeId, { message: `Attempt ${attempt}/${maxAttempts}: Script exceeded word limit. Redrafting to compress...` });
            }

            const response = await ai.models.generateContent({
                model: 'gemini-2.5-flash',
                contents: `Source Material to adapt:\n${sourceText}`,
                config: { 
                    systemInstruction: systemPrompt,
                    temperature: 0.2, 
                    topP: 0.8         
                }
            });

            finalScript = response.text;
            
            // Count the words generated
            const wordCount = finalScript.trim().split(/\s+/).length;

            if (wordCount <= 2100) {
                success = true;
            } else {
                attempt++;
            }
        }

        fs.writeFileSync(path.join(sessionDir, 'script.txt'), finalScript);
        
        if (success) {
            emitStreamLog(safeId, { message: "Script successfully drafted and formatted within limits!" });
        } else {
            // Failsafe: If it still fails after 3 tries, deliver the closest attempt so the user can manually edit
            emitStreamLog(safeId, { message: "Warning: Script generated but slightly over word limit after maximum retries. Manual editing may be required." });
        }
        
        res.json({ success: true, script: finalScript });
    } catch (error) {
        emitStreamLog(safeId, { status: 'error', message: "Failed to draft script: " + error.message });
        res.status(500).json({ error: error.message });
    }
});

module.exports = router;