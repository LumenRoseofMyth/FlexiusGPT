@echo off
REM --- Create main modules folder ---
mkdir modules

REM --- For each HIMKS kernel file, make folder, move, and add placeholders ---

REM CORE_RULES
mkdir modules\01_core_rules
move "CORE_RULES.txt" modules\01_core_rules\core_rules.txt
type nul > modules\01_core_rules\schema.md
type nul > modules\01_core_rules\README.md
type nul > modules\01_core_rules\core_rules.py

REM PHASE_MANAGER
mkdir modules\02_phase_manager
move "PHASE_MANAGER.txt" modules\02_phase_manager\phase_manager.txt
type nul > modules\02_phase_manager\schema.md
type nul > modules\02_phase_manager\README.md
type nul > modules\02_phase_manager\phase_manager.py

REM COMPLIANCE_ENGINE
mkdir modules\03_compliance_engine
move "COMPLIANCE_ENGINE.txt" modules\03_compliance_engine\compliance_engine.txt
type nul > modules\03_compliance_engine\schema.md
type nul > modules\03_compliance_engine\README.md
type nul > modules\03_compliance_engine\compliance_engine.py

REM SAFETY_OVERRIDES
mkdir modules\04_safety_overrides
move "SAFETY_OVERRIDES.txt" modules\04_safety_overrides\safety_overrides.txt
type nul > modules\04_safety_overrides\schema.md
type nul > modules\04_safety_overrides\README.md
type nul > modules\04_safety_overrides\safety_overrides.py

REM RECOVERY_STACK
mkdir modules\05_recovery_stack
move "RECOVERY_STACK.txt" modules\05_recovery_stack\recovery_stack.txt
type nul > modules\05_recovery_stack\schema.md
type nul > modules\05_recovery_stack\README.md
type nul > modules\05_recovery_stack\recovery_stack.py

REM USER_PROFILE
mkdir modules\06_user_profile
move "USER_PROFILE.txt" modules\06_user_profile\user_profile.txt
type nul > modules\06_user_profile\schema.md
type nul > modules\06_user_profile\README.md
type nul > modules\06_user_profile\user_profile.py

REM SESSION_ENGINE
mkdir modules\07_session_engine
move "SESSION_ENGINE.txt" modules\07_session_engine\session_engine.txt
type nul > modules\07_session_engine\schema.md
type nul > modules\07_session_engine\README.md
type nul > modules\07_session_engine\session_engine.py

REM FEEDBACK_ENGINE
mkdir modules\08_feedback_engine
move "FEEDBACK_ENGINE.txt" modules\08_feedback_engine\feedback_engine.txt
type nul > modules\08_feedback_engine\schema.md
type nul > modules\08_feedback_engine\README.md
type nul > modules\08_feedback_engine\feedback_engine.py

REM KNOWLEDGE_BASE
mkdir modules\09_knowledge_base
move "KNOWLEDGE_BASE.txt" modules\09_knowledge_base\knowledge_base.txt
type nul > modules\09_knowledge_base\schema.md
type nul > modules\09_knowledge_base\README.md
type nul > modules\09_knowledge_base\knowledge_base.py

REM NUTRITION_ENGINE
mkdir modules\10_nutrition_engine
move "NUTRITION_ENGINE.txt" modules\10_nutrition_engine\nutrition_engine.txt
type nul > modules\10_nutrition_engine\schema.md
type nul > modules\10_nutrition_engine\README.md
type nul > modules\10_nutrition_engine\nutrition_engine.py

REM MOTIVATION_STACK
mkdir modules\11_motivation_stack
move "MOTIVATION_STACK.txt" modules\11_motivation_stack\motivation_stack.txt
type nul > modules\11_motivation_stack\schema.md
type nul > modules\11_motivation_stack\README.md
type nul > modules\11_motivation_stack\motivation_stack.py

REM SPECIAL_POPULATIONS
mkdir modules\12_special_populations
move "SPECIAL_POPULATIONS.txt" modules\12_special_populations\special_populations.txt
type nul > modules\12_special_populations\schema.md
type nul > modules\12_special_populations\README.md
type nul > modules\12_special_populations\special_populations.py

REM DEVICE_INTEGRATION
mkdir modules\13_device_integration
move "DEVICE_INTEGRATION.txt" modules\13_device_integration\device_integration.txt
type nul > modules\13_device_integration\schema.md
type nul > modules\13_device_integration\README.md
type nul > modules\13_device_integration\device_integration.py

REM COACHING_ENGINE
mkdir modules\14_coaching_engine
move "COACHING_ENGINE.txt" modules\14_coaching_engine\coaching_engine.txt
type nul > modules\14_coaching_engine\schema.md
type nul > modules\14_coaching_engine\README.md
type nul > modules\14_coaching_engine\coaching_engine.py

REM INTEGRITY_AUDIT
mkdir modules\15_integrity_audit
move "INTEGRITY_AUDIT.txt" modules\15_integrity_audit\integrity_audit.txt
type nul > modules\15_integrity_audit\schema.md
type nul > modules\15_integrity_audit\README.md
type nul > modules\15_integrity_audit\integrity_audit.py

REM COMMUNITY_ENGINE
mkdir modules\16_community_engine
move "COMMUNITY_ENGINE.txt" modules\16_community_engine\community_engine.txt
type nul > modules\16_community_engine\schema.md
type nul > modules\16_community_engine\README.md
type nul > modules\16_community_engine\community_engine.py

REM GOAL_SETTING_ENGINE
mkdir modules\17_goal_setting_engine
move "GOAL_SETTING_ENGINE.txt" modules\17_goal_setting_engine\goal_setting_engine.txt
type nul > modules\17_goal_setting_engine\schema.md
type nul > modules\17_goal_setting_engine\README.md
type nul > modules\17_goal_setting_engine\goal_setting_engine.py

REM ACCESSIBILITY_ENGINE
mkdir modules\18_accessibility_engine
move "ACCESSIBILITY_ENGINE.txt" modules\18_accessibility_engine\accessibility_engine.txt
type nul > modules\18_accessibility_engine\schema.md
type nul > modules\18_accessibility_engine\README.md
type nul > modules\18_accessibility_engine\accessibility_engine.py

REM DATA_PRIVACY_ENGINE
mkdir modules\19_data_privacy_engine
move "DATA_PRIVACY_ENGINE.txt" modules\19_data_privacy_engine\data_privacy_engine.txt
type nul > modules\19_data_privacy_engine\schema.md
type nul > modules\19_data_privacy_engine\README.md
type nul > modules\19_data_privacy_engine\data_privacy_engine.py

REM CONTENT_UPDATE_ENGINE
mkdir modules\20_content_update_engine
move "CONTENT_UPDATE_ENGINE.txt" modules\20_content_update_engine\content_update_engine.txt
type nul > modules\20_content_update_engine\schema.md
type nul > modules\20_content_update_engine\README.md
type nul > modules\20_content_update_engine\content_update_engine.py

echo.
echo --- All 20 modules have been modularized. ---
pause
