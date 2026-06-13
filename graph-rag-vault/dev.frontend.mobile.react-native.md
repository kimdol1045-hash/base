---
id: "dev.frontend.mobile.react-native"
domain: "development.frontend"
type: "pattern"
bloom_level: ""
tags: ["frontend", "mobile", "react-native", "cross-platform"]
brain_region: "CORTEX"
token_estimate: 420
---

# dev.frontend.mobile.react-native

> #246 React Native Architecture (Meta, The New Architecture 2022)

# React Native 개발 가이드

## 핵심 원칙
- Expo를 기본 도구로 사용하여 개발 경험을 극대화한다
- 네이티브 모듈이 꼭 필요한 경우에만 Bare Workflow로 전환한다
- 플랫폼별 차이를 `Platform.OS`로 처리한다
- 성능 최적화는 FlatList와 memo를 기본으로 한다

## DO
- Expo SDK를 활용하여 카메라, 위치, 알림 등을 구현한다
- React Navigation으로 네비게이션을 구성한다
- 목록에는 반드시 `FlatList`를 사용한다 (`ScrollView` + map 금지)
- TypeScript strict 모드를 사용한다
- OTA(Over-the-Air) 업데이트를 활용한다

## DON'T
- `ScrollView` 안에 대량 데이터를 렌더링하지 않는다
- 인라인 스타일을 반복 생성하지 않는다 (`StyleSheet.create` 사용)
- JS 스레드에서 무거운 연산을 실행하지 않는다
- 웹과 동일한 CSS 단위를 사용하지 않는다 (dp 기반)

## 코드 예시
```tsx
import { FlatList, StyleSheet, Text, View, Platform } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";

interface User {
  id: string;
  name: string;
  email: string;
}

function UserItem({ user }: { user: User }) {
  return (
    <View style={styles.item}>
      <Text style={styles.name}>{user.name}</Text>
      <Text style={styles.email}>{user.email}</Text>
    </View>
  );
}

export function UserListScreen() {
  const { data, isLoading, refetch } = useUsers();

  return (
    <SafeAreaView style={styles.container}>
      <FlatList
        data={data}
        keyExtractor={(item) => item.id}
        renderItem={({ item }) => <UserItem user={item} />}
        refreshing={isLoading}
        onRefresh={refetch}
        ItemSeparatorComponent={() => <View style={styles.separator} />}
        contentContainerStyle={styles.list}
      />
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#fff" },
  list: { padding: 16 },
  item: {
    paddingVertical: 12,
    paddingHorizontal: Platform.OS === "ios" ? 16 : 12,
  },
  name: { fontSize: 16, fontWeight: "600" },
  email: { fontSize: 14, color: "#666", marginTop: 4 },
  separator: { height: 1, backgroundColor: "#eee" },
});
```
