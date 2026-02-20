# Fitness & Performance Engine

Complete training, nutrition, recovery, and body composition system. From beginner to competitive athlete — periodized programming, macro tracking, injury prevention, and race preparation. Zero dependencies.

---

## 1. Athlete Profile Brief

Before any programming, build the profile:

```yaml
athlete_profile:
  name: ""
  age:
  sex: # M/F
  height_cm:
  weight_kg:
  body_fat_pct: # estimate if unknown
  training_age_years: # how long they've been training consistently
  experience_level: # beginner (<1yr) | intermediate (1-3yr) | advanced (3-7yr) | elite (7+yr)
  
  goals:
    primary: # e.g., "lose 10kg fat", "run sub-3hr marathon", "bench 140kg", "complete Hyrox"
    secondary: # e.g., "improve energy", "build muscle", "injury prevention"
    timeline: # weeks/months to primary goal
    
  current_training:
    days_per_week:
    session_duration_min:
    modalities: [] # strength, running, cycling, swimming, HIIT, yoga, sports
    current_program: # if any
    
  constraints:
    injuries: [] # e.g., "left shoulder impingement", "knee meniscus tear 2023"
    equipment: # home gym, commercial gym, outdoor only, minimal
    schedule_restrictions: # e.g., "can only train mornings", "travel Tue-Thu"
    dietary: [] # vegetarian, vegan, halal, allergies, intolerances
    
  health:
    sleep_avg_hours:
    stress_level: # 1-10 (10 = extremely stressed)
    medications: [] # relevant ones only
    conditions: [] # e.g., "asthma", "type 2 diabetes", "hypertension"
    
  metrics:
    resting_hr:
    max_hr: # tested or 220-age estimate
    hr_zones: # if known
    1rm: # key lifts if applicable
      squat:
      bench:
      deadlift:
      ohp:
    run_benchmarks:
      mile:
      5k:
      10k:
      half_marathon:
      marathon:
```

### Experience Level Auto-Detection

| Signal | Beginner | Intermediate | Advanced | Elite |
|--------|----------|-------------|----------|-------|
| Training age | <1 year | 1-3 years | 3-7 years | 7+ years |
| Squat (M) | <1x BW | 1-1.5x BW | 1.5-2x BW | >2x BW |
| Squat (F) | <0.75x BW | 0.75-1.25x BW | 1.25-1.75x BW | >1.75x BW |
| 5K time (M) | >30 min | 22-30 min | 18-22 min | <18 min |
| 5K time (F) | >35 min | 25-35 min | 20-25 min | <20 min |
| Recovery needs | 48-72h/muscle | 48h/muscle | 24-48h/muscle | Manages load intuitively |
| Programming needs | Linear progression | Periodized blocks | Advanced periodization | Self-programmed |

---

## 2. Goal-Based Program Selection

### Program Decision Matrix

| Goal | Best Approach | Sessions/Week | Duration | Key Metric |
|------|--------------|---------------|----------|------------|
| Fat loss | Caloric deficit + resistance + LISS | 4-5 | 12-16 weeks | Body fat %, waist cm |
| Muscle gain | Progressive overload + surplus | 4-6 | 12-20 weeks | Lean mass, 1RM |
| Strength | Heavy compounds + peaking | 3-5 | 8-16 weeks | 1RM / Wilks |
| Endurance (5K-marathon) | Polarized training 80/20 | 4-6 | 12-20 weeks | Race time |
| Hyrox / hybrid | Concurrent strength + running | 5-6 | 16-24 weeks | Total Hyrox time |
| General fitness | Balanced strength + cardio | 3-4 | Ongoing | Subjective energy, metrics |
| Body recomp | Maintenance cals + high protein + resistance | 4-5 | 16-24 weeks | Mirror, measurements |
| Sport-specific | Periodized around season | 4-6 | Season-length | Sport performance |
| Injury rehab | Progressive loading + mobility | 3-5 | 6-12 weeks | Pain-free ROM |

### Periodization Models

**Linear Periodization** (beginners):
- Week 1-4: Hypertrophy (3×12 @ 65-70%)
- Week 5-8: Strength (4×6 @ 75-82%)
- Week 9-12: Power (5×3 @ 85-92%)
- Week 13: Deload (2×8 @ 50%)

**Undulating Periodization** (intermediate+):
- Monday: Heavy (5×5 @ 80-85%)
- Wednesday: Moderate (3×10 @ 70%)
- Friday: Light/Speed (4×3 @ 60% explosive)

**Block Periodization** (advanced):
- Block 1 (3-4 weeks): Accumulation — high volume, moderate intensity
- Block 2 (3-4 weeks): Transmutation — moderate volume, high intensity
- Block 3 (2-3 weeks): Realization — low volume, peak intensity
- Deload: 1 week between blocks

**Polarized (endurance)** — 80/20 rule:
- 80% of training at Zone 1-2 (easy, conversational)
- 20% at Zone 4-5 (hard intervals)
- Almost no Zone 3 ("grey zone") — it's too hard to recover from but too easy to improve

---

## 3. Training Program Templates

### 3A. Strength Program (Upper/Lower 4-Day)

```yaml
week_template:
  monday: # Upper A — Strength Focus
    - exercise: Barbell Bench Press
      sets: 4
      reps: 5
      intensity: "80-85% 1RM"
      rest: "3 min"
    - exercise: Barbell Row
      sets: 4
      reps: 6
      intensity: "75-80%"
      rest: "2-3 min"
    - exercise: Overhead Press
      sets: 3
      reps: 8
      intensity: "70-75%"
      rest: "2 min"
    - exercise: Weighted Pull-ups
      sets: 3
      reps: 6-8
      rest: "2 min"
    - exercise: Face Pulls
      sets: 3
      reps: 15
      rest: "60s"
    - exercise: Tricep Dips
      sets: 3
      reps: 8-12
      rest: "90s"

  tuesday: # Lower A — Strength Focus
    - exercise: Back Squat
      sets: 4
      reps: 5
      intensity: "80-85%"
      rest: "3-4 min"
    - exercise: Romanian Deadlift
      sets: 3
      reps: 8
      intensity: "70-75%"
      rest: "2-3 min"
    - exercise: Bulgarian Split Squat
      sets: 3
      reps: 10/leg
      rest: "90s"
    - exercise: Leg Curl
      sets: 3
      reps: 12
      rest: "60s"
    - exercise: Calf Raises
      sets: 4
      reps: 15
      rest: "60s"
    - exercise: Ab Wheel Rollout
      sets: 3
      reps: 10
      rest: "60s"

  thursday: # Upper B — Hypertrophy Focus
    - exercise: Incline Dumbbell Press
      sets: 4
      reps: 10
      intensity: "RPE 7-8"
      rest: "2 min"
    - exercise: Cable Row
      sets: 4
      reps: 10
      rest: "90s"
    - exercise: Lateral Raises
      sets: 4
      reps: 15
      rest: "60s"
    - exercise: Chin-ups
      sets: 3
      reps: 8-12
      rest: "90s"
    - exercise: Incline Curl + Overhead Tricep Extension (superset)
      sets: 3
      reps: 12
      rest: "60s"

  friday: # Lower B — Hypertrophy Focus
    - exercise: Trap Bar Deadlift
      sets: 4
      reps: 8
      intensity: "RPE 7-8"
      rest: "3 min"
    - exercise: Front Squat
      sets: 3
      reps: 8
      rest: "2-3 min"
    - exercise: Hip Thrust
      sets: 3
      reps: 12
      rest: "90s"
    - exercise: Leg Extension + Leg Curl (superset)
      sets: 3
      reps: 12
      rest: "60s"
    - exercise: Standing Calf Raise
      sets: 4
      reps: 12
      rest: "60s"
    - exercise: Hanging Leg Raise
      sets: 3
      reps: 12
      rest: "60s"
```

### 3B. Running Program (5K → Half Marathon)

**12-Week Base Building Phase:**

| Week | Easy Runs | Long Run | Intervals | Total km |
|------|-----------|----------|-----------|----------|
| 1-2 | 3 × 5km | 8km | — | 23km |
| 3-4 | 3 × 6km | 10km | 1 × 6×400m | 30km |
| 5-6 | 3 × 7km | 12km | 1 × 5×800m | 35km |
| 7-8 | 3 × 7km | 14km | 1 × 4×1km | 39km |
| 9-10 | 3 × 8km | 16km | 1 × 3×1.6km | 43km |
| 11 | 3 × 8km | 18km | 1 × 6×800m | 46km |
| 12 | 2 × 6km | 10km | 1 × 4×400m | 28km (taper) |

**Heart Rate Zone Training:**

| Zone | % Max HR | Feel | Purpose | Weekly % |
|------|----------|------|---------|----------|
| Z1 Recovery | 50-60% | Very easy, can chat freely | Active recovery | 10-15% |
| Z2 Aerobic | 60-70% | Comfortable, can hold conversation | Base building | 60-70% |
| Z3 Tempo | 70-80% | Uncomfortable, short sentences only | Lactate threshold | 5-10% |
| Z4 Threshold | 80-90% | Hard, few words | VO2max, speed | 10-15% |
| Z5 Max | 90-100% | All-out, can't talk | Race pace, sprints | 0-5% |

### 3C. Hyrox / Hybrid Program (16-Week)

```yaml
weekly_structure:
  monday: # Strength — Upper
    focus: "Push/Pull compounds"
    duration: "60 min"
    
  tuesday: # Running — Intervals
    focus: "VO2max or tempo"
    session: "8×400m @ 5K pace, 90s rest"
    duration: "45 min"
    
  wednesday: # Hyrox Stations
    focus: "2-3 stations practiced"
    stations_rotation:
      - "SkiErg 1km + Sled Push 50m"
      - "Rowing 1km + Farmers Carry 200m"
      - "Burpee Broad Jumps 80m + Wall Balls 100"
      - "Sandbag Lunges 200m + Sled Pull 50m"
    duration: "45-60 min"
    
  thursday: # Strength — Lower
    focus: "Squat/Hinge + single leg"
    duration: "60 min"
    
  friday: # Running — Easy + Strides
    focus: "Zone 2 easy + 6×100m strides"
    duration: "40-50 min"
    
  saturday: # Long Session — Hyrox Simulation
    focus: "Partial or full simulation"
    session: "4 stations with 1km runs between"
    duration: "60-90 min"
    
  sunday: # Recovery
    focus: "Active recovery or complete rest"
    options: "Walk, swim, yoga, mobility"
```

---

## 4. Progressive Overload Rules

### Strength Progression

| Level | Progression Rate | Method |
|-------|-----------------|--------|
| Beginner | +2.5kg/session (upper), +5kg/session (lower) | Linear |
| Intermediate | +2.5kg/week or +1 rep/session | Double progression |
| Advanced | +2.5-5kg/mesocycle (3-4 weeks) | Block periodization |

**Double Progression Protocol:**
1. Set a rep range (e.g., 3×8-12)
2. Start at bottom of range with challenging weight
3. Add 1 rep per session until top of range on all sets
4. Increase weight by 2.5-5kg, drop back to bottom of range
5. Repeat

**When Progress Stalls (>2 weeks no improvement):**
1. Check recovery first (sleep, nutrition, stress)
2. Deload for 1 week (50% volume)
3. Change rep scheme (switch from 5×5 to 3×8)
4. Swap exercise variation (flat bench → incline)
5. If still stalled after 4 weeks: change program

### Endurance Progression

- **10% Rule**: Increase weekly volume by no more than 10%
- **3-week build, 1-week back-off** cycle
- Never increase intensity AND volume in the same week
- Add a new run day only after current days feel sustainable for 3+ weeks

---

## 5. Nutrition Framework

### Calorie Targets

**Step 1 — BMR (Mifflin-St Jeor):**
- Male: BMR = (10 × weight_kg) + (6.25 × height_cm) - (5 × age) + 5
- Female: BMR = (10 × weight_kg) + (6.25 × height_cm) - (5 × age) - 161

**Step 2 — TDEE (Activity Multiplier):**

| Activity | Multiplier | Description |
|----------|-----------|-------------|
| Sedentary | 1.2 | Desk job, no exercise |
| Light | 1.375 | 1-3 days/week |
| Moderate | 1.55 | 3-5 days/week |
| Active | 1.725 | 6-7 days/week |
| Very Active | 1.9 | 2x/day or physical job + training |

**Step 3 — Goal Adjustment:**

| Goal | Calorie Target | Rate | Duration |
|------|---------------|------|----------|
| Aggressive cut | TDEE - 750 | ~0.7kg/week | 8-12 weeks max |
| Moderate cut | TDEE - 500 | ~0.5kg/week | 12-16 weeks |
| Slow cut (preserve muscle) | TDEE - 300 | ~0.3kg/week | 16-24 weeks |
| Maintenance | TDEE | — | Ongoing |
| Lean bulk | TDEE + 200-300 | ~0.25kg/week | 16-24 weeks |
| Aggressive bulk | TDEE + 500 | ~0.5kg/week | 12-16 weeks |
| Recomp | TDEE (± 100) | Scale stable | 24+ weeks |

### Macronutrient Targets

| Macro | Fat Loss | Muscle Gain | Endurance | Maintenance |
|-------|----------|-------------|-----------|-------------|
| Protein | 2.0-2.4g/kg | 1.8-2.2g/kg | 1.4-1.8g/kg | 1.6-2.0g/kg |
| Fat | 0.8-1.0g/kg | 0.8-1.2g/kg | 1.0-1.2g/kg | 0.8-1.2g/kg |
| Carbs | Remainder | Remainder | Remainder (prioritize) | Remainder |

**Protein Rules:**
- Spread across 3-5 meals (30-50g per meal for muscle protein synthesis)
- Within 2 hours post-training (protein + carbs)
- Before bed: slow protein (casein, Greek yogurt) if optimizing
- Minimum per meal: 0.4g/kg bodyweight

**Carb Timing for Performance:**
- Pre-workout (1-2h before): 1-2g/kg — oats, rice, banana
- Intra-workout (>90 min sessions): 30-60g/hr — sports drink, gels
- Post-workout (within 1h): 1-1.5g/kg — rice, potato, fruit
- Rest of day: distribute evenly

### Meal Planning Template

```yaml
meal_plan:
  meal_1_breakfast:
    time: "07:00"
    example: "3 eggs + 2 toast + avocado + fruit"
    protein_g: 25
    carbs_g: 45
    fat_g: 20
    calories: 460

  meal_2_lunch:
    time: "12:00"
    example: "Chicken breast 200g + rice 150g (dry) + vegetables + olive oil"
    protein_g: 50
    carbs_g: 55
    fat_g: 15
    calories: 555

  meal_3_pre_workout:
    time: "15:30"
    example: "Greek yogurt 200g + banana + honey + oats 40g"
    protein_g: 25
    carbs_g: 60
    fat_g: 5
    calories: 385

  meal_4_post_workout:
    time: "18:30"
    example: "Salmon 200g + sweet potato 250g + broccoli"
    protein_g: 45
    carbs_g: 50
    fat_g: 18
    calories: 540

  meal_5_evening:
    time: "21:00"
    example: "Casein shake + peanut butter + berries"
    protein_g: 35
    carbs_g: 15
    fat_g: 12
    calories: 310

  daily_totals:
    protein_g: 180
    carbs_g: 225
    fat_g: 70
    calories: 2250
```

### Supplement Stack (Evidence-Based Only)

| Supplement | Dose | Timing | Evidence Level | Purpose |
|-----------|------|--------|---------------|---------|
| Creatine monohydrate | 5g/day | Any time | ⭐⭐⭐⭐⭐ | Strength, power, lean mass |
| Caffeine | 3-6mg/kg | 30-60 min pre-workout | ⭐⭐⭐⭐⭐ | Performance, focus |
| Vitamin D3 | 2000-5000 IU | With fat-containing meal | ⭐⭐⭐⭐ | Immune, bone, mood (if deficient) |
| Omega-3 (EPA/DHA) | 2-3g combined | With meal | ⭐⭐⭐⭐ | Inflammation, recovery |
| Magnesium | 200-400mg | Before bed | ⭐⭐⭐⭐ | Sleep, recovery, cramping |
| Whey protein | As needed | Post-workout or meals | ⭐⭐⭐⭐ | Convenience, hitting protein target |
| Electrolytes | As needed | During long sessions | ⭐⭐⭐ | Hydration (>60 min or heat) |

**Skip these** (weak/no evidence for healthy people): BCAAs (if eating enough protein), testosterone boosters, fat burners, glutamine.

---

## 6. Recovery & Sleep

### Recovery Priority Stack

| Priority | Factor | Target | Impact |
|----------|--------|--------|--------|
| 1 | Sleep | 7-9 hours | Highest — nothing replaces it |
| 2 | Nutrition | Hit protein + calories | Fuels adaptation |
| 3 | Stress management | Daily practice | Cortisol kills gains |
| 4 | Active recovery | 2-3x/week | Light movement, walking |
| 5 | Hydration | 0.033L/kg + 500ml/hr training | Often overlooked |
| 6 | Mobility work | 10-15 min daily | Injury prevention |
| 7 | Massage/foam rolling | 1-2x/week | Minor benefit, feels good |
| 8 | Cold/heat exposure | Optional | Marginal, context-dependent |

### Sleep Optimization Checklist

- [ ] Consistent bed/wake time (±30 min, even weekends)
- [ ] Room temperature 16-19°C
- [ ] Complete darkness (blackout curtains/eye mask)
- [ ] No screens 30-60 min before bed (or use blue light filter)
- [ ] No caffeine after 2 PM (or 8-10 hours before bed)
- [ ] No alcohol within 3 hours of bed (disrupts deep sleep)
- [ ] Last meal 2-3 hours before bed
- [ ] Magnesium before bed (glycinate or threonate)
- [ ] Morning sunlight within 30 min of waking (circadian anchor)
- [ ] Wind-down routine: reading, stretching, breathing exercises

### Deload Protocol

**When to deload** (any 2 of these):
- Performance declining for 2+ weeks
- Persistent fatigue, poor sleep, irritability
- Joint/tendon soreness that doesn't resolve with rest
- Motivation dropping significantly
- After 4-6 weeks of hard training (planned)

**How to deload (pick one):**
- **Volume deload**: Same weight, 50% fewer sets
- **Intensity deload**: Same sets/reps, 60% of normal weight
- **Active recovery week**: Replace training with walking, swimming, yoga
- **Duration**: 5-7 days

### Overtraining Warning Signs

| Stage | Signals | Action |
|-------|---------|--------|
| Overreaching (normal) | Temporary fatigue, slight performance dip | Continue — adaptation coming |
| Functional overreaching | Fatigue lasting >1 week, motivation dropping | Deload 1 week |
| Non-functional overreaching | Performance drop >2 weeks, sleep disrupted, mood changes | 2 weeks off, reassess volume |
| Overtraining syndrome | Chronic fatigue, illness, depression, injury | Medical review, extended rest (months) |

---

## 7. Injury Prevention & Management

### Pre-Workout Warm-Up (10 min)

```
1. General (3 min): Light cardio — rowing, cycling, or brisk walk
2. Dynamic stretching (3 min):
   - Leg swings (10/side)
   - Hip circles (10/side)
   - Arm circles (10 each direction)
   - Inchworms (5)
   - World's greatest stretch (5/side)
3. Activation (2 min):
   - Band pull-aparts (15)
   - Glute bridges (15)
   - Dead bugs (10/side)
4. Movement prep (2 min):
   - Empty bar/light weight sets of first exercise
   - Ramp up: 50% × 5, 70% × 3, 85% × 1
```

### Common Injury Decision Tree

```
Pain during exercise?
├── Sharp/acute pain → STOP immediately → RICE → See physio if persists >3 days
├── Dull ache that warms up → Modify (reduce weight 20%, avoid end-range) → Monitor
├── Pain only after → Usually DOMS or inflammation → Ice, mobility, reduce volume
└── Chronic nagging pain (>2 weeks) → See physio → Don't train through it

Joint vs Muscle pain?
├── Joint: More concerning — reduce load, check form, see professional
└── Muscle: Usually recoverable — DOMS peaks at 24-72h, persistent = potential strain
```

### Movement Substitution Table

| If THIS hurts | Try THIS instead |
|--------------|-----------------|
| Barbell back squat (low back) | Front squat, goblet squat, leg press |
| Flat bench press (shoulder) | Floor press, neutral-grip DB press, landmine press |
| Conventional deadlift (low back) | Trap bar deadlift, Romanian DL, hip thrust |
| Overhead press (shoulder) | Landmine press, high incline press |
| Barbell row (low back) | Chest-supported row, cable row, machine row |
| Running (knee/shin) | Cycling, swimming, elliptical, rowing |
| Pull-ups (elbow) | Neutral-grip pull-ups, lat pulldown, band-assisted |

---

## 8. Body Composition Tracking

### Measurement Protocol

**Weekly (same conditions every time):**
- Weight: Morning, after bathroom, before food/water, same scale
- Take average of 7 daily weigh-ins — single days mean nothing

**Bi-weekly:**
- Waist circumference (at navel, relaxed)
- Hip circumference (widest point)
- Optional: chest, arms, thighs

**Monthly:**
- Progress photos (front, side, back — same lighting, same time)
- Strength benchmarks (test or estimate 1RM)
- Endurance benchmarks (time trial or test set)

### Interpreting Progress

| Weight | Waist | Strength | What's Happening | Action |
|--------|-------|----------|-----------------|--------|
| ↓ | ↓ | → or ↑ | Fat loss, muscle maintained ✅ | Continue |
| ↓ | → | ↓ | Losing muscle ❌ | Increase protein, reduce deficit |
| ↑ | → | ↑ | Lean gain ✅ | Continue |
| ↑ | ↑ | ↑ | Gaining fat + muscle | Reduce surplus slightly |
| → | ↓ | ↑ | Recomposition ✅ | Continue — this is ideal |
| → | → | → | Plateau | Change something — calories, program, or both |
| ↑ | ↑ | → | Just getting fat ❌ | Reduce calories, increase activity |

### Rate of Weight Change (Healthy Ranges)

| Goal | Male | Female | If faster than this |
|------|------|--------|-------------------|
| Fat loss | 0.5-1% BW/week | 0.5-0.8% BW/week | Losing muscle — slow down |
| Muscle gain | 0.25-0.5% BW/month | 0.15-0.25% BW/month | Gaining fat — reduce surplus |

---

## 9. Training Log & Tracking

### Session Log Template

```yaml
session:
  date: "YYYY-MM-DD"
  type: # strength | cardio | hybrid | recovery
  duration_min:
  sleep_hours_last_night:
  energy_level: # 1-10
  
  exercises:
    - name: ""
      sets:
        - { reps: , weight_kg: , rpe: }
        - { reps: , weight_kg: , rpe: }
      notes: ""
      
  cardio:
    type: # run | bike | row | swim
    duration_min:
    distance_km:
    avg_hr:
    avg_pace:
    zone_distribution: # e.g., "80% Z2, 20% Z4"
    
  post_session:
    overall_rating: # 1-10
    what_went_well: ""
    what_to_improve: ""
    pain_or_discomfort: ""
```

### Weekly Review Questions

1. Did I hit all planned sessions? If not, why?
2. Did any lifts progress (weight or reps)?
3. Was my energy consistently good? (If not → check sleep, nutrition, stress)
4. Any pain or discomfort developing?
5. Am I recovering between sessions?
6. Bodyweight trend this week? (7-day average vs last week)
7. Am I enjoying training? (Burnout check)

### Monthly Review

```yaml
monthly_review:
  month: "YYYY-MM"
  sessions_completed: # / planned
  adherence_pct:
  
  strength_progress:
    squat: { start: , end: , change: }
    bench: { start: , end: , change: }
    deadlift: { start: , end: , change: }
    
  body_comp:
    weight_start:
    weight_end:
    waist_start:
    waist_end:
    
  endurance:
    weekly_km_avg:
    best_5k:
    best_10k:
    
  energy_avg: # 1-10
  sleep_avg:
  
  wins: []
  lessons: []
  next_month_focus: ""
```

---

## 10. RPE & Autoregulation

### RPE (Rate of Perceived Exertion) Scale

| RPE | Description | Reps in Reserve |
|-----|-------------|-----------------|
| 10 | Absolute max, couldn't do 1 more | 0 RIR |
| 9.5 | Might get 1 more on a great day | 0-1 RIR |
| 9 | Could definitely get 1 more | 1 RIR |
| 8.5 | Could get 1-2 more | 1-2 RIR |
| 8 | Could get 2 more | 2 RIR |
| 7.5 | Could get 2-3 more | 2-3 RIR |
| 7 | Could get 3 more, good working weight | 3 RIR |
| 6 | Warm-up feel, speed work | 4+ RIR |

**RPE Targets by Training Phase:**
- Hypertrophy: RPE 7-8.5 (2-3 RIR)
- Strength: RPE 8-9.5 (0-2 RIR)
- Peaking: RPE 9-10
- Deload: RPE 5-6

### Daily Readiness Check

Before training, assess (30 seconds):

| Factor | Green (train as planned) | Yellow (reduce 10-20%) | Red (easy session or rest) |
|--------|------------------------|----------------------|--------------------------|
| Sleep | 7+ hours, woke refreshed | 5-7 hours | <5 hours |
| Soreness | None or mild | Moderate, functional | Severe, limits movement |
| Motivation | Excited to train | Neutral | Dreading it |
| Stress | Normal | Elevated | Overwhelming |
| HRV/RHR | Normal range | Slightly off | Significantly elevated |

**2+ Reds = rest day or active recovery. Don't fight your body.**

---

## 11. Race & Competition Prep

### Taper Protocol (Endurance)

| Weeks Out | Volume Reduction | Intensity | Notes |
|-----------|-----------------|-----------|-------|
| 3 | -20% | Maintain | Last long run |
| 2 | -40% | Maintain | Short sharp intervals OK |
| 1 | -60% | 2 easy runs + race pace strides | Rest, sleep, hydrate |
| Race week | -80% | Race day | Trust the training |

### Race Day Checklist

- [ ] Nutrition: Nothing new on race day — practice in training
- [ ] Last big meal: night before (carb-heavy, low fiber)
- [ ] Race morning: 2-3h before start, familiar meal (toast + banana + coffee)
- [ ] Hydration: Sip water morning, don't overdrink
- [ ] Warm-up: 10-15 min easy jog + 4×100m strides
- [ ] Pacing: Start conservative, negative split if possible
- [ ] Fueling (>60 min): 30-60g carbs/hour from gels/drink

### Strength Competition Prep (Powerlifting)

| Weeks Out | Focus | Intensity | Volume |
|-----------|-------|-----------|--------|
| 8-6 | Volume accumulation | 70-80% | High |
| 6-4 | Intensity build | 80-90% | Moderate |
| 4-2 | Peak singles/doubles | 90-100% | Low |
| 1 | Openers only | 85-90% | Minimal |
| Meet week | Rest + opener walkthrough | — | — |

**Attempt Selection:**
- Opener: Something you can triple any day (90-92%)
- Second: Goal PR or comfortable single (95-97%)
- Third: Stretch PR (100-103%)

---

## 12. Special Populations & Adaptations

### Training Over 40

- Warm-ups take longer — add 5-10 min
- Recovery takes longer — space hard sessions 48-72h
- Joint health priority — more machine work, less maximal lifting
- Focus: strength maintenance, mobility, cardiovascular health
- Deload more frequently (every 3 weeks instead of 4-6)

### Training While Traveling

- **Hotel room workout (no equipment):**
  - Push-ups (4×max), Pike push-ups (3×10), Bulgarian split squats (3×12/leg)
  - Single-leg RDL (3×10/leg), Plank (3×45s), Burpees (3×10)
- **Minimal equipment (bands):**
  - Add banded rows, banded squats, banded face pulls
- **Priority order:** Sleep > nutrition > some exercise > perfect exercise

### Female-Specific Considerations

- **Menstrual cycle training:**
  - Follicular phase (day 1-14): Higher tolerance for volume and intensity
  - Ovulation (day 14): Peak strength potential
  - Luteal phase (day 15-28): May need to reduce intensity, increase rest
  - Menstruation (day 1-5): Train by feel — some women perform fine, others need lighter days
- **Iron**: Monitor if heavy periods — supplement if ferritin <30
- **Calorie floor**: Never go below 1200 kcal — hormonal disruption risk

---

## 13. Habit Building & Consistency

### The 2-Minute Rule
If motivation is zero, commit to just 2 minutes of the workout. Once you start, you'll usually continue. If you genuinely stop after 2 minutes — that's fine, you maintained the habit.

### Minimum Effective Dose
When life gets chaotic, don't skip — scale down:

| Full Session | Minimum Version | Time |
|-------------|----------------|------|
| 60 min strength | 3 compound lifts, 3×5 | 20 min |
| 10km run | 20 min easy jog | 20 min |
| Full Hyrox sim | 1 station + 1km run | 15 min |
| Meal prep Sunday | Cook 1 protein in bulk | 30 min |

### Streak Protection
- **Never miss twice in a row** — one skip is rest, two is a pattern
- **Anchor to existing habit** — gym bag by the door, workout clothes laid out
- **Remove friction** — gym close to home/work, meals prepped, plan written

---

## 14. Common Mistakes

| Mistake | Why It Hurts | Fix |
|---------|-------------|-----|
| No progressive overload | Body adapts, stops improving | Track every session, add weight/reps |
| Too much volume too soon | Injury, burnout | 10% weekly increase max |
| Skipping deloads | Accumulated fatigue, plateau | Planned deload every 4-6 weeks |
| Not eating enough protein | Poor recovery, muscle loss | 1.6-2.2g/kg minimum |
| Cardio killing gains | Excessive interference | Separate by 6+ hours or different days |
| Program hopping | Never adapting to stimulus | Stick with program 8-12 weeks minimum |
| Ignoring sleep | #1 recovery killer | 7-9 hours non-negotiable |
| All-or-nothing mindset | Miss one day → miss the week | Minimum effective dose instead |
| Comparing to others | Demotivation | Compare to last month's you |
| No tracking | Can't improve what you don't measure | Log sessions + nutrition |

---

## 15. Natural Language Commands

Use conversational requests:

| Command | What It Does |
|---------|-------------|
| "Build me a training program" | Creates periodized program from athlete profile |
| "Calculate my macros" | Computes TDEE + macro split for goal |
| "Write me a meal plan" | Generates daily meal plan hitting macro targets |
| "Review my training week" | Analyzes session logs, flags issues |
| "Am I overtraining?" | Checks recovery signals against overtraining markers |
| "Substitute [exercise]" | Finds alternatives based on injury/equipment |
| "Plan my race taper" | Creates taper protocol for upcoming race |
| "Track my body composition" | Interprets weight/measurement trends |
| "Create a deload week" | Generates deload based on current program |
| "What should I eat before my workout?" | Pre-workout nutrition based on session type + timing |
| "Help me break through a plateau" | Diagnoses stall + provides program adjustments |
| "Build a home workout" | No-equipment or minimal-equipment session |

---

## 16. Quick Reference Cards

### The Big 5 Lifts — Cue Cheat Sheet

| Lift | Setup Cues | Execution Cues | Common Fault |
|------|-----------|----------------|-------------|
| Squat | Feet shoulder-width, toes 15-30° out, bar on traps | Brace core, break at hips + knees, knees track toes | Knees caving in → cue "spread the floor" |
| Bench | Eyes under bar, arch + retract scapulae, feet flat | Unrack, lower to nipple line, drive through feet | Flared elbows → tuck 45° |
| Deadlift | Bar over mid-foot, hip-width stance, grip outside knees | Push floor away, bar drags shins, lockout hips | Rounding lower back → brace harder, drop hips |
| OHP | Bar on front delts, grip just outside shoulders | Brace glutes, press straight up, head through | Leaning back → squeeze glutes tighter |
| Row | Hinge 45°, arms hang, pull to lower chest | Lead with elbows, squeeze shoulder blades, control down | Using momentum → lighter weight, pause at top |

---

*Built by AfrexAI — the AI-native consultancy. This is what we automate for businesses across 10 industries.*
