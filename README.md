# base_project

## 概要

プロジェクトのテンプレートです。  
データベース接続、コンフィグ設定、通知などの機能を備えています。

## 使用方法

本プロジェクトのエントリポイントは`base_project/cli.py`です。  
引数を設定することで、`base_project/main`配下のプログラムを実行します。
```bash
python cli.py <module_path> <class_name> [<args>]
```

| 引数 | 説明 |
| --- | --- |
| module_path | 呼び出す主処理のファイルパスを`.`で連結(例: base_project.main.sample.sample)　|
| class_name | 呼び出すクラス(例: Sample) |
| [\<args>\] | 個別の処理で設定するコマンドライン引数 |

呼び出すクラスは、`base_project/main/base/base/BasicLogic`を継承するする必要があります。  
具体的な例は、`base_project/main/sample`です。

