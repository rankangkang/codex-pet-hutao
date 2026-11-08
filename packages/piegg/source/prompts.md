# 皮蛋素材制作提示词

使用内置 imagegen。参考为用户提供的第二张皮蛋照片；原始照片未复制进仓库。先生成透明全身基准，再以照片和基准生成各动作条。

## 透明基准

> This is a fidelity-critical photo cutout edit, not a character redesign. Use the supplied NEW photograph as the sole source. Isolate the exact real black-and-tan Shiba Inu puppy and its entire visible cowboy outfit from the room and floor, and make all background genuinely transparent. Preserve the puppy's individual face, natural small dark eyes, black fur and subtle grey-tan cheek and brow markings, ear shape, closed mouth, neutral expression, original sitting pose, paws, lighting, proportions and photographic fur texture as closely as possible to the source. Preserve the actual outfit: yellow checked panels, red neckerchief with white floral pattern, black-and-white cow-print vest, blue strap, gold buttons and sheriff star. Do not invent a bow, flower, tongue, blush, cartoon outlines, toy-like eyes, grin, different colors, accessories or a new pose. Retain the complete paws and silhouette as photographed; do not reshape the head or eyes, or make it cuter. Only remove the room, floor and cast shadow, with clean transparent edges around the fur. Center the full-body cutout on a square transparent canvas with comfortable padding. No checkerboard, backdrop, text, duplicated dogs, outlines or floating decorations.

## 动作条共同要求

> Fidelity-critical sprite animation of the exact same real puppy in the first reference photo; the second image is a transparent pose guide. Match the real individual dog's small dark eyes, closed mouth, black fur, subtle grey-tan brows/cheeks, upright ears, puppy proportions and realistic photo texture, without beautifying, cartoonizing, orange tint or changing its face. Preserve its exact red floral neckerchief, yellow check shoulders, blue strap and gold buttons, black-and-white cow print vest and gold sheriff star. No bows, flower on ears, blush, added ornaments, toys, text, floor, shadow or motion graphics. One ultra-wide 3:1 horizontal strip against solid pure bright green #00FF00 edge to edge. Every full puppy is separated in one horizontal row in its own evenly spaced invisible slot, all same size, full ears, body and paws visible, with space between. Green exists only in the background: no green light, reflections or color spill on the puppy, outfit or paws.

各行动作要求：

- `idle`：6 帧正面坐姿，轻微呼吸、眨眼并回到起始姿势。
- `walking-right`、`walking-left`：各 8 帧四足向屏幕右侧、左侧自然行走，交替迈步。
- `waving`：4 帧正面坐姿，前爪放下、抬起、举起、放回。
- `jumping`：5 帧，坐姿、蹲下、小跳、下落、回到坐姿，保留真实的垂直位移。
- `failed`：8 帧轻微低头、放松耳朵、眨眼并回到平静状态。
- `waiting`：6 帧轻微歪头、竖耳、眨眼并回到起始姿势。
- `licking`：6 帧闭嘴、露舌尖、短暂舔鼻、收回并恢复闭嘴。
- `review`：6 帧注视屏幕左侧、回中、注视右侧、回中。

## 注视方向

> Create a very wide 3:1 horizontal row of exactly eight complete separate full-body poses of the same real black-and-tan Shiba puppy in the first reference photo; the second reference is the neutral pose. Preserve the exact facial identity, small natural dark eyes, subtle muted tan markings, closed mouth, black fur, photorealism, natural proportions and cowboy vest: red floral scarf, yellow checks, cow-print fabric, gold star and buttons. Absolutely no bows or added accessories. All eight are seated in an identical fixed front-facing position with the same stable body size and paws on the same baseline. Change only gaze direction through natural eyes and a small head orientation as requested; the resulting directions should be visibly different. Screen directions are relative to the viewer. Exactly eight distinct evenly spaced poses, in one row, separated by generous background, no overlaps or crops. Background is flat pure green #00FF00 edge to edge with no green reflected on the dog. No text, numbers, arrows, grid, icons, floor, shadow, duplicated eyes, new props or outline.

- `gaze-0-7`：上、上偏右、右上、右偏上、右、右偏下、右下、下偏右。
- `gaze-8-15`：下、下偏左、左下、左偏下、左、左偏上、左上、上偏左。
