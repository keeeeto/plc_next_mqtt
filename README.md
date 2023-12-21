## MqttTag Library

## Topic  
すべてのtopicはmqtt_tag/の下にあります。例:mqtt_tag/alive
* alive
  * 起動してからの時間。
  * 名前ごとの時間ではなくあくまでそのマイコンの起動からの時間であるため途中で名前を変更した場合は注意が必要。
  * 例:(topic)mqtt_tag/alive/255 (payload)1132 とは255という名前で登録されたマイコンの起動からの時間が1132msということ
  * 1HzでPublishされる
* change_tag_name  
　 * 名前が変更されたときに変更される前の名前がPublishされる 255->aabbに変更された場合255がPublishされる
* finish_tag  
　 * buzzer呼び出しされた後ボダンが押されbuzzer呼び出しが完了したときにPublishされる
　* payloadは完了したデバイスの名前である 
* buzzer_code  
　 * MastterデバイスからPublishする必要があるtopic
　* このtopicのpayloadに呼び出したいデバイス名を入れると　ブザーで呼び出される。
　* finish_tagで完了を検知したら速やかにpayloadをnullにする or　ほかの名前を入れる
　* じゃいないと永遠に呼び出しループされてしまう
