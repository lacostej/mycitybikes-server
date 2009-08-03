mkdir -f generated
./test/convert_android_assets.py STOCKHOLM_PROVIDER_ID ./assets/stockholm.xml > generated/stockholm.xml
./test/convert_android_assets.py OSLO_PROVIDER_ID ./assets/oslo.xml > generated/oslo.xml
