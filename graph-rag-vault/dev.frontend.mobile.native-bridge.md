---
id: "dev.frontend.mobile.native-bridge"
domain: "development.frontend"
type: "pattern"
bloom_level: ""
tags: ["frontend", "mobile", "native-bridge", "react-native"]
brain_region: "CORTEX"
token_estimate: 420
---

# dev.frontend.mobile.native-bridge

> #249 Native Bridge Pattern (React Native New Architecture, Meta 2022)

# 네이티브 브릿지(Native Bridge) 가이드

## 핵심 원칙
- JavaScript와 네이티브 코드(Swift/Kotlin) 간 통신을 브릿지로 처리한다
- Expo Modules API를 우선 사용하고, 불가능할 때만 직접 브릿지를 작성한다
- 브릿지 호출은 비동기로 설계하여 UI 스레드를 블로킹하지 않는다
- New Architecture(Fabric + TurboModules)를 활용하여 성능을 개선한다

## DO
- Expo Modules API로 네이티브 기능을 래핑한다
- 데이터 직렬화 오버헤드를 최소화한다 (큰 데이터는 참조 전달)
- 네이티브 이벤트를 EventEmitter로 JS에 전달한다
- 네이티브 모듈의 타입을 TypeScript로 정의한다

## DON'T
- UI 스레드에서 무거운 브릿지 호출을 동기적으로 수행하지 않는다
- 대용량 데이터를 JSON 직렬화로 브릿지를 통해 전달하지 않는다
- 네이티브 코드 없이 해결 가능한 기능에 브릿지를 사용하지 않는다
- Old Architecture의 Bridge를 새 프로젝트에서 사용하지 않는다

## 코드 예시
```typescript
// Expo Module (TypeScript + Swift)
// modules/my-sensor/index.ts
import { NativeModulesProxy, EventEmitter } from "expo-modules-core";

const MySensorModule = NativeModulesProxy.MySensor;
const emitter = new EventEmitter(MySensorModule);

export function startSensor(interval: number): void {
  MySensorModule.start(interval);
}

export function stopSensor(): void {
  MySensorModule.stop();
}

export function onSensorData(callback: (data: SensorData) => void) {
  return emitter.addListener("onSensorData", callback);
}

interface SensorData {
  x: number;
  y: number;
  z: number;
  timestamp: number;
}
```

```swift
// modules/my-sensor/ios/MySensorModule.swift
import ExpoModulesCore
import CoreMotion

public class MySensorModule: Module {
  let motionManager = CMMotionManager()

  public func definition() -> ModuleDefinition {
    Name("MySensor")

    Function("start") { (interval: Double) in
      self.motionManager.accelerometerUpdateInterval = interval / 1000
      self.motionManager.startAccelerometerUpdates(to: .main) { data, _ in
        guard let data = data else { return }
        self.sendEvent("onSensorData", [
          "x": data.acceleration.x,
          "y": data.acceleration.y,
          "z": data.acceleration.z,
          "timestamp": Date().timeIntervalSince1970,
        ])
      }
    }

    Function("stop") {
      self.motionManager.stopAccelerometerUpdates()
    }

    Events("onSensorData")
  }
}
```
