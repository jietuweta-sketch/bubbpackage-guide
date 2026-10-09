# 指南站每日文章维护与发布

## 工作位置和频率

唯一日常维护仓库：E:\Codex\GitHub\bubbpackage-guide。旧 WSL 仓库保留作备份，不再日常维护。不修改主站首页。每天北京时间9:00写公司新闻、行业动态、知识文章各2篇，共6篇。文件分别放 articles/company、articles/industry、articles/knowledge。

## 文章结构

统一的只有 Markdown 开头元信息 title、date、category、summary、published、cover。正文根据选题自由组织，不固定段落数量、小标题或结尾。日期用本站发布日期，新闻事件日期在正文写清。文件名用小写英文和中划线，不以下划线开头；避免与 company、industry、knowledge 同名。

近30天选题、结构和核心论点去重，不以改写旧标题充数；同日重跑检查现有文章和日志，仅补未完成部分。每天轮换图文解析、问答、对比表、清单、流程、真实数据分析、案例示意等形式，六篇不得套同一结构。形式服从内容，不强制每篇都有图片、表格或数据。

## 事实与来源

公司新闻仅依据真实更新、已核实的平台功能或用户提供事实。没有真实新事件时，可发表明确标注为平台服务介绍或使用说明的内容，不虚构公司新闻、客户、订单、销量、报价、交期、认证或评价。行业动态必须浏览可信一手来源，写明来源链接和事件日期，不将旧事件冒充当天新闻。知识文章给出可操作方法和边界。

所有数字、法规和时效性论断查证，注明来源、统计年份、单位、地域与适用范围。不能虚构数据、实测和新闻。例子或测算说明假设，分析与源事实分开。不抄袭或大段复制来源。

## 图片与表格

配图使用有授权素材、自制图表示意或依适用 imagegen 技能生成的图片，保存 assets/article-images/YYYY-MM-DD/ 下，并写有意义的替代文字、图注、来源或设计示意说明。AI效果图不可冒充实拍、真实客户或出货证据。不热链来源图片，不生成虚构图表数据。

正文图片示例：![盒型结构示意](/assets/article-images/2026-10-10/box-layout.png)。表格使用 Markdown 表格，数值有来源或明确假设；图片、表格与主题有关。

## Windows 环境与发布

使用 PowerShell，所有 Git 操作明确仓库路径。Python使用 .venv/Scripts/python.exe。依赖缺失时执行 .venv/Scripts/python.exe -m pip install -r scripts/article-requirements.txt。

1. git status，若有不属于本次任务的修改，保留并避免夹带。git pull --ff-only，不覆盖本地改动、不强推。
2. 写入当天六篇与配图，published 为 true；保留草稿则写 false。
3. .venv/Scripts/python.exe scripts/build_articles.py build。
4. node scripts/validate_guides.mjs；git diff --check；检查新文章数量、来源、日期、元信息、图片与内部链接。校验正文包含有意义的内容并完成必要的版面检查。
5. 仅 add 本批 Markdown、配图及生成的 news 文件和 sitemap.xml；commit并push origin main。用户已授权自动发布，每天不重复询问。
6. 检查 GitHub Publish Markdown articles 与 Pages 发布成功，线上新页面、feed.json/feed.js包含新文章；失败保留成果并报告原因。
7. 本地 .automation/article-log.json 记录日期、选题、形式、来源、路径、提交和发布结果；同日恢复避免重复。

## 执行报告

每天一批，完成即结束。成功简短报告6篇标题和线上链接；等待或无变化时保持安静，失败或需要用户输入时说明具体原因。不要无期限轮询，不用静默成功冒充验证成功。
