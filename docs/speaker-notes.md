# Speaker Notes — ADA Compliance Auditor (3 min)

## Slide 1: Title
**[JERRISON]**: "Hi everyone, I'm Jerrison, this is Malik. We built an AI that looks at a photo of your building and tells you exactly where you're breaking ADA law — before a plaintiff's attorney does it for you."

## Slide 2: The Problem
**[JERRISON]**: "Eight thousand six hundred sixty-seven ADA lawsuits last year. California alone — thirty-eight percent of the nation. Each visit to a non-compliant business is a separate four-thousand-dollar violation under the Unruh Act. Meanwhile, there are only 900 certified inspectors for four million California businesses. The math doesn't work. That's the gap we fill."

## Slide 3: Who It Hurts
**[MALIK]**: "Seventy million Americans have a disability. They control four hundred ninety billion in purchasing power. But only twenty-three percent are employed, compared to sixty-five percent of the general population. Inaccessible spaces are the barrier. And for businesses — one lawsuit averages sixteen thousand dollars in settlement alone, before legal fees. This problem hurts everyone."

## Slide 4: How It Works
**[MALIK]**: "Here's how it works. Take a photo of your building entrance, parking lot, restroom — anything. RocketRide processes the address to determine your state jurisdiction and applicable building codes. Then Gemini Vision runs three passes: classify the scene, detect violations against fifty-one types with visual cues, then verify everything for consistency. You get a prioritized report with exact ADA code references, severity, cost to fix, and step-by-step remediation. Five seconds, not five weeks."

## Slide 5: What Makes Us Different
**[JERRISON]**: "There are tools for website accessibility. There are expensive human inspectors with months-long waitlists. But nobody has built an AI that analyzes a photo of a physical space for ADA violations. We're the first. Fifty-one violation types, mapped to federal ADA, California Building Code, and local ordinances for seven cities. This category didn't exist until we built it."

## Slide 6: Architecture — RocketRide + Gemini
**[JERRISON]**: "Under the hood, RocketRide is our pipeline orchestration engine. We define the workflow as a visual directed graph in VS Code — address processing flows through RocketRide's pipeline, then Gemini Vision handles the three-pass image analysis. The pipeline is defined in a .pipe file and executed via the Python SDK from our FastAPI backend. This separates pipeline design from application code."

## Slide 7: Market & Business Model
**[MALIK]**: "The accessibility market is growing from one-point-four billion to three-point-two billion by 2034. We're starting with small businesses who can't afford a CASp inspection but definitely can't afford a lawsuit. Per-scan for individuals, subscription for ongoing monitoring, and API for enterprise. There is no grandfather clause in ADA — compliance is required, every year, forever."

## Slide 8: Try It Live / Q&A
**[JERRISON]**: "We have a live demo running right now. Scan the QR code — upload any photo and see the analysis in real time."

**[MALIK]**: "We'd love your questions. And if you're a property owner — try it on your own building. You might be surprised what it finds."

**[JERRISON]**: "Thanks everyone."
