### 配置文件结构
```
{
    log: {
        console: [{
                sink: String
                level: Int
                serialize: bool
                format: String
                rotation: Int | String
                retention: Int | String
        }]
        stat: [{
                sink: String
                format: String
                rotation: Int | String
                retention: Int | String
        }]
    }
    quotas: {
        enable: {
            cpu: bool
            disk: bool
            mem: bool
            ...
        }
    }
    threshold: {
        ...
    }
    report: {
        enable: {
            email: bool
            webhook: bool
            ...
        }
        email: {
            host: String
            user: String
            pass: String
            sender: String
            targets: [{
                receiver: String
            }]
        }
        webhook: {
            targets: [{
                endpoint: String
                placeholder: String
                template: String
                headers: dict
            }]
        }
        ...
    }
}
```