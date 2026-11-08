# 皮蛋像素版：素材提示词

使用内置 imagegen，以用户提供的第二张照片为参考；原始照片未复制进仓库。先生成透明的像素全身基准，再用基准生成动作条。

## 全身基准

> Create one full-body, cartoon pixel-art desktop pet based on the actual Shiba Inu puppy in the supplied photo. It must still be recognizably the same puppy: compact seated four-legged black Shiba pup, upright triangular ears, small dark eyes, subtle grey-tan eyebrows and cheeks, cream-grey muzzle and paws, naturally closed little mouth and the same quiet expression. Match the exact cowboy outfit: yellow checked shoulders, red neckerchief with white flowers, black-and-white cow-print vest, blue strap, round gold buttons and gold sheriff star. No bow or flower on its ears, no human body, no extra accessories. Use charming, crisp, hand-drawn 16-bit pixel art with intentionally large square pixels, a restrained cohesive palette, simple dark outlines and clustered pixel shading, readable at 192x208 display size. Cute cartoon proportions are fine but do not over-enlarge eyes or add an exaggerated grin. Show the entire puppy including all visible paws, centered and complete, with generous margin on a genuinely transparent background. No backdrop, checkerboard, floor, shadow, text, effects, logos, or extra characters.

## 动作条共同要求

> Create one ultra-wide 3:1 horizontal sprite animation strip. Only the same 16-bit pixel-art black Shiba puppy from the supplied reference. Preserve its pixel style, palette, small dark eyes, upright ears, grey-tan cheeks and paws, red floral scarf, yellow checked shoulders, blue strap, cow-print vest, gold button and sheriff star. Crisp large square pixels, no blur or realistic fur. No bow. Background is perfectly flat pure green #00FF00 edge to edge, with no green on the character. Place separate full-body puppies at the same scale in one horizontal row of evenly spaced invisible slots with complete ears, body, paws, and no overlap. No text, grid, borders, shadows, scenery, detached effects or motion marks.

各行动作要求：

- `idle`：6 帧坐姿，轻微呼吸、眨眼并回到起始姿势。
- `walking-right`、`walking-left`：各 8 帧四足侧向行走，分别面向屏幕右侧、左侧。
- `waving`：4 帧坐姿抬起一只前爪再放下。
- `jumping`：5 帧坐姿、蹲下、小跳、下落、回到坐姿。
- `failed`：8 帧轻微低头、放松耳朵并恢复。
- `waiting`：6 帧轻微歪头、听声音、眨眼并恢复。
- `licking`：6 帧闭嘴、露舌尖、短暂舔鼻、收回并恢复闭嘴。
- `review`：6 帧自然转头向左、回中、向右、回中，保持深色小眼睛。

## 注视方向

> Very wide 3:1 horizontal row of exactly eight complete, separated full-body sprites of the same pixel-art black Shiba puppy in the reference. Maintain the reference's pixel clusters, small dark eyes and expression, muted tan brows and cheeks, black fur, red floral scarf, yellow checks, cow print vest, gold star and buttons. All dogs are seated at the same scale with paws planted at the same baseline. Express direction with a natural small head orientation, while keeping the small dark eyes true to the reference: no big eye whites, no googly eyes, no cartoon face distortion. One horizontal row, separated by flat pure green #00FF00 background, no text, arrows, frames, shadow, additional accessories or objects.

- `gaze-0-7`：上、上偏右、右上、右偏上、右、右偏下、右下、下偏右。
- `gaze-8-15`：下、下偏左、左下、左偏下、左、左偏上、左上、上偏左。
