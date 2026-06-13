---
id: "dev.frontend.mobile.touch-interaction"
domain: "development.frontend"
type: "pattern"
bloom_level: ""
tags: ["frontend", "mobile", "touch", "gesture", "ux"]
brain_region: "CORTEX"
token_estimate: 400
---

# dev.frontend.mobile.touch-interaction

> #248 Touch Interaction Design (Apple HIG, Google Material Design 3)

# 터치 인터랙션 가이드

## 핵심 원칙
- 터치 대상은 최소 44x44px (iOS) / 48x48dp (Android)를 유지한다
- 제스처는 직관적이고 되돌릴 수 있어야 한다
- 시각적 피드백을 즉시 제공한다 (탭 → 하이라이트)
- 실수로 인한 의도치 않은 동작을 방지한다

## DO
- 스와이프, 드래그 등 제스처에 애니메이션 피드백을 제공한다
- 삭제 같은 위험한 동작에 확인 단계를 추가한다
- Pull-to-Refresh 패턴을 목록에 구현한다
- 엣지 스와이프(뒤로 가기)를 네이티브 제스처와 충돌하지 않게 한다

## DON'T
- 호버(hover) 전용 인터랙션을 터치 환경에서 사용하지 않는다
- 더블탭을 유일한 인터랙션 수단으로 사용하지 않는다
- 스크롤 영역 안에 스와이프 제스처를 중첩하지 않는다
- 터치 대상 간 간격을 8px 미만으로 하지 않는다

## 코드 예시
```tsx
// React Native 스와이프 삭제
import { Swipeable } from "react-native-gesture-handler";
import Animated from "react-native-reanimated";

function SwipeableRow({ children, onDelete }: SwipeableRowProps) {
  const renderRightActions = (progress: Animated.SharedValue<number>) => (
    <Animated.View style={[styles.deleteAction, { opacity: progress }]}>
      <Text style={styles.deleteText}>삭제</Text>
    </Animated.View>
  );

  return (
    <Swipeable
      renderRightActions={renderRightActions}
      onSwipeableOpen={() => {
        Alert.alert("삭제", "정말 삭제하시겠습니까?", [
          { text: "취소", style: "cancel" },
          { text: "삭제", style: "destructive", onPress: onDelete },
        ]);
      }}
    >
      {children}
    </Swipeable>
  );
}

// 웹 터치 대상 크기 보장 (Tailwind)
function IconButton({ icon, onClick, label }: IconButtonProps) {
  return (
    <button
      onClick={onClick}
      aria-label={label}
      className="min-h-[44px] min-w-[44px] flex items-center justify-center
                 rounded-full active:bg-gray-100 transition-colors"
    >
      {icon}
    </button>
  );
}
```
