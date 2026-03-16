# WeryAI Image Skill

<description>
Generates high-quality AI images from text prompts via WeryAI API.
</description>

<capabilities>
- Text-to-Image generation
</capabilities>

<usage>
```bash
node /Users/king/weryai-image-skill/weryai-generate.js "<english_prompt>"
```
</usage>

<rules>
1. Always translate the user's prompt to English before execution.
2. Provide specific, detailed, and visually descriptive prompts for best results.
3. The script will output "Success! Result: <URL>".
4. Render the returned URL as a markdown image `![Generated Image](<URL>)` in the final response.
</rules>