#!/bin/sh

zip -q -r amiyabot-plugin-config-demo-1.1.zip *
rm -rf ../../amiya-bot-v6/plugins/amiyabot-plugin-config-demo-*
mv amiyabot-plugin-config-demo-*.zip ../../amiya-bot-v6/plugins/
docker restart amiya-bot 