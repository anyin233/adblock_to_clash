# Adblock规则到Clash规则转换器

该项目使用一个配置文件存放所有待转换的Adblock格式的配置文件，配置文件格式如下

```yaml
rules:
- nsfw.oisd.nl 
- https://cdn.jsdelivr.net/gh/hagezi/dns-blocklists@latest/adblock/nsfw.txt
target: clash
```

其中rules中每一项是一个用于下载规则的链接，target表示其目标是转换为clash的ruleset格式

## 要求

1. 转换目标是clash的ruleset格式，需要可以直接被clash使用
2. 转换的过程中需要对规则进行去重
