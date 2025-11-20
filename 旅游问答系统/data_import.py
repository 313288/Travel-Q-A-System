from neo4j import GraphDatabase
from config import NEO4J_CONFIG

class Neo4jDataImporter:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def clear_database(self):
        """清空数据库（测试用）"""
        with self.driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")
            print("数据库已清空")

    def import_data(self):
        """导入测试旅游数据（修正Cypher语法错误）"""
        with self.driver.session() as session:
            # 1. 创建城市节点（单个语句，多个节点用逗号分隔）
            session.run("""
                CREATE 
                (bj:City {name: '北京', level: '一线城市', description: '中国首都，历史文化名城'}),
                (sh:City {name: '上海', level: '一线城市', description: '中国经济中心，国际化大都市'})
                
            """)

            # 2. 创建景点节点（单个语句）
            session.run("""
                CREATE 
                (gugong:Attraction {name: '故宫', type: '人文景观', rating: 4.9, opening_hours: '8:30-17:00（16:30停止入场）'}),
                (changcheng:Attraction {name: '长城', type: '自然+人文景观', rating: 4.8, opening_hours: '7:30-18:00'}),
                (waitan:Attraction {name: '外滩', type: '人文景观', rating: 4.8, opening_hours: '全天开放'})
            """)

            # 3. 创建美食、住宿、交通节点（单个语句）
            session.run("""
                CREATE 
                (kaoya:Food {name: '北京烤鸭', type: '京菜', price_range: '中高', description: '皮脆肉嫩'}),
                (xiaolongbao:Food {name: '小笼包', type: '沪菜', price_range: '中', description: '皮薄汁多'}),
                (beijing_fandian:Accommodation {name: '北京饭店', type: '五星级酒店', price_range: '高', rating: 4.7}),
                (shanghai_fandian:Accommodation {name: '上海外滩茂悦酒店', type: '五星级酒店', price_range: '高', rating: 4.6}),
                (ditie1:Transportation {name: '地铁1号线', type: '地铁', route: '苹果园-四惠东', price: '3-10元'}),
                (ditie2:Transportation {name: '地铁2号线', type: '地铁', route: '徐泾东-浦东国际机场', price: '3-12元'})
            """)

            # 4. 创建关系：景点→城市（单个语句）
            session.run("""
                MATCH (a:Attraction), (c:City)
                WHERE (a.name IN ['故宫', '长城'] AND c.name = '北京') OR (a.name = '外滩' AND c.name = '上海')
                CREATE (a)-[:LOCATED_IN]->(c)
            """)

            # 5. 创建关系：城市→推荐美食（单个语句，修正冗余关系定义）
            session.run("""
                MATCH (c:City {name: '北京'}), (f:Food {name: '北京烤鸭'})
                CREATE (c)-[:RECOMMENDS_FOOD]->(f)
            """)
            session.run("""
                MATCH (c:City {name: '上海'}), (f:Food {name: '小笼包'})
                CREATE (c)-[:RECOMMENDS_FOOD]->(f)
            """)

            # 6. 创建关系：景点→附近美食（单个语句）
            session.run("""
                MATCH (a:Attraction {name: '故宫'}), (f:Food {name: '北京烤鸭'})
                CREATE (a)-[:NEAR_FOOD {distance: '1km'}]->(f)
            """)
            session.run("""
                MATCH (a:Attraction {name: '外滩'}), (f:Food {name: '小笼包'})
                CREATE (a)-[:NEAR_FOOD {distance: '0.8km'}]->(f)
            """)

            # 7. 可选：创建景点→附近住宿、城市→交通关系（扩展功能）
            session.run("""
                MATCH (a:Attraction {name: '故宫'}), (ac:Accommodation {name: '北京饭店'})
                CREATE (a)-[:NEAR_ACCOMMODATION {distance: '2km'}]->(ac)
            """)
            session.run("""
                MATCH (c:City {name: '北京'}), (t:Transportation {name: '地铁1号线'})
                CREATE (c)-[:HAS_TRANSPORTATION]->(t)
            """)

        print("数据导入完成！")

    def import_hefei_data(self):
        """导入合肥旅游数据（修正Cypher语法错误）"""
        with self.driver.session() as session:
            # 1. 创建城市节点（单个语句，多个节点用逗号分隔）
            session.run("""
                CREATE 
                (hf:City {name: '合肥', level: '新一线城市', description: '长三角城市群副中心，科教基地，创新之都'})
            """)

            # 2. 创建景点节点（单个语句）
            session.run("""
                CREATE 
                (sanhe:Attraction {name: '三河古镇', type: '人文景观', rating: 4.5, opening_hours: '8:00 - 17:30'}),
                (binhu:Attraction {name: '合肥滨湖国家森林公园', type: '自然景观', rating: 4.7, opening_hours: '全天开放'})
            """)

            # 3. 创建美食、住宿、交通节点（单个语句）
            session.run("""
                CREATE 
                (xiaolongxia:Food {name: '合肥小龙虾', type: '徽菜/地方菜', price_range: '中', description: '鲜香麻辣，夜宵王牌'}),
                (caocaoji:Food {name: '曹操鸡', type: '徽菜', price_range: '中高', description: '肉质鲜嫩，药膳同源'}),
                (junyue:Accommodation {name: '合肥君悦酒店', type: '五星级酒店', price_range: '高', rating: 4.7}),
                (bailinglangting:Accommodation {name: '合肥栢景朗廷酒店', type: '五星级酒店', price_range: '高', rating: 4.6}),
                (ditie1:Transportation {name: '合肥地铁1号线', type: '地铁', route: '张洼-九联圩', price: '2-5元'}),
                (jichangbash:Transportation {name: '新桥机场巴士', type: '机场巴士', route: '市区-新桥机场', price: '25元'})
            """)

            # 4. 创建关系：景点→城市（单个语句）
            session.run("""
                MATCH (a:Attraction), (c:City {name: '合肥'})
                WHERE a.name IN ['三河古镇', '合肥滨湖国家森林公园']
                CREATE (a)-[:LOCATED_IN]->(c)
            """)

            # 5. 创建关系：城市→推荐美食（单个语句，修正冗余关系定义）
            session.run("""
                MATCH (c:City {name: '合肥'}), (f:Food)
                WHERE f.name IN ['合肥小龙虾', '曹操鸡']
                CREATE (c)-[:RECOMMENDS_FOOD]->(f)
            """)

            # 6. 创建关系：景点→附近美食（单个语句）
            session.run("""
                MATCH (a:Attraction {name: '三河古镇'}), (f:Food)
                WHERE f.name IN ['合肥小龙虾', '曹操鸡']
                CREATE (a)-[:NEAR_FOOD {distance: '1.5km'}]->(f)
            """)
            session.run("""
                MATCH (a:Attraction {name: '合肥滨湖国家森林公园'}), (f:Food {name: '合肥小龙虾'})
                CREATE (a)-[:NEAR_FOOD {distance: '3km'}]->(f)
            """)

            # 7. 可选：创建景点→附近住宿、城市→交通关系（扩展功能）
            session.run("""
                MATCH (a:Attraction {name: '三河古镇'}), (ac:Accommodation {name: '合肥君悦酒店'})
                CREATE (a)-[:NEAR_ACCOMMODATION {distance: '8km'}]->(ac)
            """)
            session.run("""
                MATCH (a:Attraction {name: '合肥滨湖国家森林公园'}), (ac:Accommodation {name: '合肥栢景朗廷酒店'})
                CREATE (a)-[:NEAR_ACCOMMODATION {distance: '5km'}]->(ac)
            """)
            session.run("""
                MATCH (c:City {name: '合肥'}), (t:Transportation)
                WHERE t.name IN ['合肥地铁1号线', '新桥机场巴士']
                CREATE (c)-[:HAS_TRANSPORTATION]->(t)
            """)

        print("合肥旅游数据导入完成！")

    def import_bengbu_data(self):
        """导入蚌埠旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
                CREATE 
                (bb:City {name: '蚌埠', level: '三线城市', description: '淮河流域中心城市，禹会诸侯地，交通枢纽'})
            """)

            # 2. 创建景点节点
            session.run("""
                CREATE 
                (longzihu:Attraction {name: '龙子湖风景区', type: '自然景观', rating: 4.5, opening_hours: '全天开放'}),
                (zhanggongshan:Attraction {name: '张公山公园', type: '自然+人文景观', rating: 4.4, opening_hours: '8:00 - 18:00'})
            """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
                CREATE 
                (shaobingjialiji:Food {name: '烧饼夹里脊', type: '地方小吃', price_range: '低', description: '酥香可口，地方标志'}),
                (hugoushaobing:Food {name: '湖沟烧饼', type: '地方小吃', price_range: '低', description: '香酥多层，远近闻名'}),

                (wandajiahua:Accommodation {name: '蚌埠万达嘉华酒店', type: '五星级酒店', price_range: '中高', rating: 4.5}),
                (jianguofandian:Accommodation {name: '蚌埠建国饭店', type: '豪华型酒店', price_range: '中', rating: 4.4}),

                (gongjiao:Transportation {name: '蚌埠公交', type: '公交', route: '覆盖全市', price: '1-2元'}),
                (nanzhan:Transportation {name: '蚌埠南站', type: '高铁站', route: '京沪高铁沿线', price: '-'})
            """)

            # 4. 创建关系：景点→城市
            session.run("""
                MATCH (a:Attraction), (c:City {name: '蚌埠'})
                WHERE a.name IN ['龙子湖风景区', '张公山公园']
                CREATE (a)-[:LOCATED_IN]->(c)
            """)

            # 5. 创建关系：城市→推荐美食
            session.run("""
                MATCH (c:City {name: '蚌埠'}), (f:Food)
                WHERE f.name IN ['烧饼夹里脊', '湖沟烧饼']
                CREATE (c)-[:RECOMMENDS_FOOD]->(f)
            """)

            # 6. 创建关系：景点→附近美食
            session.run("""
                MATCH (a:Attraction {name: '张公山公园'}), (f:Food {name: '烧饼夹里脊'})
                CREATE (a)-[:NEAR_FOOD {distance: '0.8km'}]->(f)
            """)
            session.run("""
                MATCH (a:Attraction {name: '龙子湖风景区'}), (f:Food {name: '湖沟烧饼'})
                CREATE (a)-[:NEAR_FOOD {distance: '2km'}]->(f)
            """)

            # 7. 创建关系：景点→附近住宿、城市→交通
            session.run("""
                MATCH (a:Attraction {name: '龙子湖风景区'}), (ac:Accommodation {name: '蚌埠万达嘉华酒店'})
                CREATE (a)-[:NEAR_ACCOMMODATION {distance: '3km'}]->(ac)
            """)
            session.run("""
                MATCH (a:Attraction {name: '张公山公园'}), (ac:Accommodation {name: '蚌埠建国饭店'})
                CREATE (a)-[:NEAR_ACCOMMODATION {distance: '2.5km'}]->(ac)
            """)
            session.run("""
                MATCH (c:City {name: '蚌埠'}), (t:Transportation)
                WHERE t.name IN ['蚌埠公交', '蚌埠南站']
                CREATE (c)-[:HAS_TRANSPORTATION]->(t)
            """)
            session.run("""
                MATCH (a:Attraction {name: '龙子湖风景区'}), (t:Transportation {name: '蚌埠公交'})
                CREATE (a)-[:NEAR_TRANSPORTATION {distance: '0.5km'}]->(t)
            """)

        print("蚌埠旅游数据导入完成！")

    def import_wuhu_data(self):
        """导入芜湖旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
                CREATE 
                (wh:City {name: '芜湖', level: '三线城市', description: '安徽省域副中心城市，江东名邑，创新之城'})
            """)

            # 2. 创建景点节点
            session.run("""
                CREATE 
                (fangte:Attraction {name: '芜湖方特旅游区', type: '主题乐园', rating: 4.8, opening_hours: '9:00 - 18:00 (季节调整)'}),
                (jiuziguangchang:Attraction {name: '鸠兹广场 & 镜湖', type: '自然+人文景观', rating: 4.6, opening_hours: '全天开放'})
            """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
                CREATE 
                (xiazimian:Food {name: '芜湖虾籽面', type: '地方小吃', price_range: '低', description: '面条筋道，汤味极鲜'}),
                (wudaibanya:Food {name: '无为板鸭', type: '徽菜/地方菜', price_range: '中低', description: '先熏后卤，香气浓郁'}),

                (xilton:Accommodation {name: '芜湖世茂希尔顿酒店', type: '五星级酒店', price_range: '中高', rating: 4.6}),
                (huayi:Accommodation {name: '芜湖华邑酒店', type: '豪华型酒店', price_range: '中高', rating: 4.7}),

                (guidao1:Transportation {name: '芜湖轨道交通1号线', type: '单轨', route: '白马山-保顺路', price: '2-7元'}),
                (jichangdaba:Transportation {name: '芜宣机场大巴', type: '大巴', route: '机场-市区', price: '20元'})
            """)

            # 4. 创建关系：景点→城市
            session.run("""
                MATCH (a:Attraction), (c:City {name: '芜湖'})
                WHERE a.name IN ['芜湖方特旅游区', '鸠兹广场 & 镜湖']
                CREATE (a)-[:LOCATED_IN]->(c)
            """)

            # 5. 创建关系：城市→推荐美食
            session.run("""
                MATCH (c:City {name: '芜湖'}), (f:Food)
                WHERE f.name IN ['芜湖虾籽面', '无为板鸭']
                CREATE (c)-[:RECOMMENDS_FOOD]->(f)
            """)

            # 6. 创建关系：景点→附近美食
            session.run("""
                MATCH (a:Attraction {name: '鸠兹广场 & 镜湖'}), (f:Food {name: '芜湖虾籽面'})
                CREATE (a)-[:NEAR_FOOD {distance: '0.3km'}]->(f)
            """)
            session.run("""
                MATCH (a:Attraction {name: '芜湖方特旅游区'}), (f:Food {name: '无为板鸭'})
                CREATE (a)-[:NEAR_FOOD {distance: '4km'}]->(f)
            """)

            # 7. 创建关系：景点→附近住宿、城市→交通及交通换乘关系
            session.run("""
                MATCH (a:Attraction {name: '鸠兹广场 & 镜湖'}), (ac:Accommodation {name: '芜湖世茂希尔顿酒店'})
                CREATE (a)-[:NEAR_ACCOMMODATION {distance: '0.8km'}]->(ac)
            """)
            session.run("""
                MATCH (a:Attraction {name: '芜湖方特旅游区'}), (ac:Accommodation {name: '芜湖华邑酒店'})
                CREATE (a)-[:NEAR_ACCOMMODATION {distance: '3.5km'}]->(ac)
            """)
            session.run("""
                MATCH (c:City {name: '芜湖'}), (t:Transportation)
                WHERE t.name IN ['芜湖轨道交通1号线', '芜宣机场大巴']
                CREATE (c)-[:HAS_TRANSPORTATION]->(t)
            """)
            session.run("""
                MATCH (t1:Transportation {name: '芜湖轨道交通1号线'}), (t2:Transportation {name: '芜宣机场大巴'})
                CREATE (t1)-[:TRANSFER_TO {note: '便捷换乘'}]->(t2)
            """)

        print("芜湖旅游数据导入完成！")

    def import_huainan_data(self):
        """导入淮南旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
                CREATE 
                (hn:City {name: '淮南', level: '四线城市', description: '中国能源之都，豆腐发源地，淮河之滨'})
            """)

            # 2. 创建景点节点
            session.run("""
                CREATE 
                (bagong:Attraction {name: '八公山国家地质公园', type: '自然+人文景观', rating: 4.4, opening_hours: '8:00-17:30'}),
                (jiaogang:Attraction {name: '焦岗湖影视城', type: '人文景观', rating: 4.2, opening_hours: '9:00-17:00'})
            """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
                CREATE 
                (niuroutang:Food {name: '淮南牛肉汤', type: '地方小吃', price_range: '低', description: '汤味醇厚，粉丝爽滑'}),
                (doufuyan:Food {name: '豆腐宴', type: '地方菜', price_range: '中', description: '豆腐发源地，做法多样'}),

                (xinjinjiang:Accommodation {name: '淮南新锦江大酒店', type: '高档型酒店', price_range: '中', rating: 4.3}),
                (guyangguoji:Accommodation {name: '淮南古阳国际大酒店', type: '豪华型酒店', price_range: '中', rating: 4.2}),

                (gongjiao:Transportation {name: '淮南公交', type: '公交', route: '覆盖全市', price: '1-2元'}),
                (dongzhan:Transportation {name: '淮南东站', type: '高铁站', route: '商合杭高铁沿线', price: '按里程计费'})
            """)

            # 4. 创建关系：景点→城市
            session.run("""
                MATCH (a:Attraction), (c:City {name: '淮南'})
                WHERE a.name IN ['八公山国家地质公园', '焦岗湖影视城']
                CREATE (a)-[:LOCATED_IN]->(c)
            """)

            # 5. 创建关系：城市→推荐美食
            session.run("""
                MATCH (c:City {name: '淮南'}), (f:Food)
                WHERE f.name IN ['淮南牛肉汤', '豆腐宴']
                CREATE (c)-[:RECOMMENDS_FOOD]->(f)
            """)

            # 6. 创建关系：景点→附近美食（含豆腐文化关联）
            session.run("""
                MATCH (a:Attraction {name: '八公山国家地质公园'}), (f:Food)
                WHERE f.name IN ['淮南牛肉汤', '豆腐宴']
                CREATE (a)-[:NEAR_FOOD {distance: '1km', note: '可了解豆腐发源历史'}]->(f)
            """)
            session.run("""
                MATCH (a:Attraction {name: '焦岗湖影视城'}), (f:Food {name: '淮南牛肉汤'})
                CREATE (a)-[:NEAR_FOOD {distance: '3.5km'}]->(f)
            """)

            # 7. 创建关系：景点→附近住宿、城市→交通
            session.run("""
                MATCH (a:Attraction {name: '八公山国家地质公园'}), (ac:Accommodation {name: '淮南新锦江大酒店'})
                CREATE (a)-[:NEAR_ACCOMMODATION {distance: '4km'}]->(ac)
            """)
            session.run("""
                MATCH (a:Attraction {name: '焦岗湖影视城'}), (ac:Accommodation {name: '淮南古阳国际大酒店'})
                CREATE (a)-[:NEAR_ACCOMMODATION {distance: '5km'}]->(ac)
            """)
            session.run("""
                MATCH (c:City {name: '淮南'}), (t:Transportation)
                WHERE t.name IN ['淮南公交', '淮南东站']
                CREATE (c)-[:HAS_TRANSPORTATION]->(t)
            """)
            session.run("""
                MATCH (a:Attraction {name: '八公山国家地质公园'}), (t:Transportation {name: '淮南公交'})
                CREATE (a)-[:NEAR_TRANSPORTATION {distance: '0.8km'}]->(t)
            """)

        print("淮南旅游数据导入完成！")

    def import_maanshan_data(self):
        """导入马鞍山旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
                CREATE 
                (mas:City {name: '马鞍山', level: '四线城市', description: '钢城，诗城，南京都市圈城市'})
            """)

            # 2. 创建景点节点
            session.run("""
                CREATE 
                (caishiji:Attraction {name: '采石矶', type: '自然+人文景观', rating: 4.6, opening_hours: '8:00-17:30'}),
                (putang:Attraction {name: '濮塘国家度假公园', type: '自然景观', rating: 4.3, opening_hours: '全天开放'})
            """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
                CREATE 
                (koudaiya:Food {name: '口袋鸭', type: '地方菜', price_range: '中', description: '汤汁浓郁，营养丰富'}),
                (caishijichagan:Food {name: '采石矶茶干', type: '地方小吃', price_range: '低', description: '口感细腻，五香风味'}),

                (haiwaihai:Accommodation {name: '马鞍山海外海皇冠假日酒店', type: '五星级酒店', price_range: '中高', rating: 4.5}),
                (jinyingshangmei:Accommodation {name: '马鞍山金鹰尚美酒店', type: '豪华型酒店', price_range: '中', rating: 4.4}),

                (dongzhan:Transportation {name: '马鞍山东站', type: '高铁站', route: '宁安高铁沿线', price: '按里程计费'}),
                (gongjiao:Transportation {name: '马鞍山公交', type: '公交', route: '覆盖全市', price: '1-2元'})
            """)

            # 4. 创建关系：景点→城市
            session.run("""
                MATCH (a:Attraction), (c:City {name: '马鞍山'})
                WHERE a.name IN ['采石矶', '濮塘国家度假公园']
                CREATE (a)-[:LOCATED_IN]->(c)
            """)

            # 5. 创建关系：城市→推荐美食
            session.run("""
                MATCH (c:City {name: '马鞍山'}), (f:Food)
                WHERE f.name IN ['口袋鸭', '采石矶茶干']
                CREATE (c)-[:RECOMMENDS_FOOD]->(f)
            """)

            # 6. 创建关系：景点→附近美食
            session.run("""
                MATCH (a:Attraction {name: '采石矶'}), (f:Food)
                WHERE f.name IN ['口袋鸭', '采石矶茶干']
                CREATE (a)-[:NEAR_FOOD {distance: '1.2km'}]->(f)
            """)
            session.run("""
                MATCH (a:Attraction {name: '濮塘国家度假公园'}), (f:Food {name: '口袋鸭'})
                CREATE (a)-[:NEAR_FOOD {distance: '5km'}]->(f)
            """)

            # 7. 创建关系：景点→附近住宿、城市→交通及高铁特色关联
            session.run("""
                MATCH (a:Attraction {name: '采石矶'}), (ac:Accommodation {name: '马鞍山金鹰尚美酒店'})
                CREATE (a)-[:NEAR_ACCOMMODATION {distance: '3km'}]->(ac)
            """)
            session.run("""
                MATCH (a:Attraction {name: '濮塘国家度假公园'}), (ac:Accommodation {name: '马鞍山海外海皇冠假日酒店'})
                CREATE (a)-[:NEAR_ACCOMMODATION {distance: '8km'}]->(ac)
            """)
            session.run("""
                MATCH (c:City {name: '马鞍山'}), (t:Transportation)
                WHERE t.name IN ['马鞍山东站', '马鞍山公交']
                CREATE (c)-[:HAS_TRANSPORTATION]->(t)
            """)
            session.run("""
                MATCH (t:Transportation {name: '马鞍山东站'})
                CREATE (t)-[:HIGH_SPEED_ROUTE {note: '至南京仅需十余分钟'}]->(:City {name: '南京'})
            """)

        print("马鞍山旅游数据导入完成！")

    def import_huaibei_data(self):
        """导入淮北旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
                CREATE 
                (hb:City {name: '淮北', level: '五线城市', description: '运河故里，能源之城'})
            """)

            # 2. 创建景点节点
            session.run("""
                CREATE 
                (xiangshan:Attraction {name: '相山公园', type: '自然景观', rating: 4.5, opening_hours: '全天开放'}),
                (nanhu:Attraction {name: '南湖公园', type: '自然景观', rating: 4.3, opening_hours: '全天开放'})
            """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
                CREATE 
                (nanpingxiangdu:Food {name: '南坪响肚', type: '地方菜', price_range: '中', description: '口感爽脆，风味独特'}),
                (huaibeitangmian:Food {name: '淮北烫面', type: '地方小吃', price_range: '低', description: '面条筋道，汤汁鲜美'}),

                (bairuite:Accommodation {name: '淮北伯瑞特酒店', type: '豪华型酒店', price_range: '中', rating: 4.4}),
                (kouziguojida:Accommodation {name: '淮北口子国际大酒店', type: '高档型酒店', price_range: '中', rating: 4.3}),

                (gongjiao:Transportation {name: '淮北公交', type: '公交', route: '覆盖全市', price: '1-2元'}),
                (beizhan:Transportation {name: '淮北北站', type: '高铁站', route: '郑徐高铁沿线', price: '按里程计费'})
            """)

            # 4. 创建关系：景点→城市
            session.run("""
                MATCH (a:Attraction), (c:City {name: '淮北'})
                WHERE a.name IN ['相山公园', '南湖公园']
                CREATE (a)-[:LOCATED_IN]->(c)
            """)

            # 5. 创建关系：城市→推荐美食
            session.run("""
                MATCH (c:City {name: '淮北'}), (f:Food)
                WHERE f.name IN ['南坪响肚', '淮北烫面']
                CREATE (c)-[:RECOMMENDS_FOOD]->(f)
            """)

            # 6. 创建关系：景点→附近美食
            session.run("""
                MATCH (a:Attraction {name: '相山公园'}), (f:Food)
                WHERE f.name IN ['南坪响肚', '淮北烫面']
                CREATE (a)-[:NEAR_FOOD {distance: '1.5km'}]->(f)
            """)
            session.run("""
                MATCH (a:Attraction {name: '南湖公园'}), (f:Food {name: '淮北烫面'})
                CREATE (a)-[:NEAR_FOOD {distance: '3km'}]->(f)
            """)

            # 7. 创建关系：景点→附近住宿、城市→交通及南湖公园特色
            session.run("""
                MATCH (a:Attraction {name: '相山公园'}), (ac:Accommodation {name: '淮北伯瑞特酒店'})
                CREATE (a)-[:NEAR_ACCOMMODATION {distance: '2km'}]->(ac)
            """)
            session.run("""
                MATCH (a:Attraction {name: '南湖公园'}), (ac:Accommodation {name: '淮北口子国际大酒店'})
                CREATE (a)-[:NEAR_ACCOMMODATION {distance: '4km', note: '国家级城市湿地公园'}]->(ac)
            """)
            session.run("""
                MATCH (c:City {name: '淮北'}), (t:Transportation)
                WHERE t.name IN ['淮北公交', '淮北北站']
                CREATE (c)-[:HAS_TRANSPORTATION]->(t)
            """)
            session.run("""
                MATCH (a:Attraction {name: '南湖公园'})
                SET a.features = '采煤塌陷区治理而成的国家级城市湿地公园'
            """)

        print("淮北旅游数据导入完成！")

    def import_tongling_data(self):
        """导入铜陵旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
                CREATE 
                (tl:City {name: '铜陵', level: '五线城市', description: '中国古铜都，当代铜基地'})
            """)

            # 2. 创建景点节点
            session.run("""
                CREATE 
                (tianjinghu:Attraction {name: '天井湖公园', type: '自然景观', rating: 4.4, opening_hours: '全天开放'}),
                (fushan:Attraction {name: '浮山风景区', type: '自然+人文景观', rating: 4.5, opening_hours: '8:00-17:00'})
            """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
                CREATE 
                (datongchagan:Food {name: '大通茶干', type: '地方小吃', price_range: '低', description: '质地柔韧，味道鲜美'}),
                (tonglingbaijiang:Food {name: '铜陵白姜', type: '地方特产', price_range: '中低', description: '肉质脆嫩，姜香浓郁'}),

                (yongquannongzhuang:Accommodation {name: '铜陵永泉农庄度假村', type: '度假酒店', price_range: '中', rating: 4.5}),
                (yidunguoj:Accommodation {name: '铜陵逸顿国际酒店', type: '豪华型酒店', price_range: '中', rating: 4.3}),

                (tonglingzhan:Transportation {name: '铜陵站', type: '火车站', route: '宁安高铁、铜九铁路', price: '按里程计费'}),
                (tonglinggj:Transportation {name: '铜陵公交', type: '公交', route: '覆盖全市', price: '1-2元'})
            """)

            # 4. 创建关系：景点→城市
            session.run("""
                MATCH (a:Attraction), (c:City {name: '铜陵'})
                WHERE a.name IN ['天井湖公园', '浮山风景区']
                CREATE (a)-[:LOCATED_IN]->(c)
            """)

            # 5. 创建关系：城市→推荐美食
            session.run("""
                MATCH (c:City {name: '铜陵'}), (f:Food)
                WHERE f.name IN ['大通茶干', '铜陵白姜']
                CREATE (c)-[:RECOMMENDS_FOOD]->(f)
            """)

            # 6. 创建关系：景点→附近美食
            session.run("""
                MATCH (a:Attraction {name: '天井湖公园'}), (f:Food)
                WHERE f.name IN ['大通茶干', '铜陵白姜']
                CREATE (a)-[:NEAR_FOOD {distance: '1.8km'}]->(f)
            """)
            session.run("""
                MATCH (a:Attraction {name: '浮山风景区'}), (f:Food {name: '大通茶干'})
                CREATE (a)-[:NEAR_FOOD {distance: '6km'}]->(f)
            """)

            # 7. 创建关系：景点→附近住宿、城市→交通及浮山特色
            session.run("""
                MATCH (a:Attraction {name: '天井湖公园'}), (ac:Accommodation {name: '铜陵逸顿国际酒店'})
                CREATE (a)-[:NEAR_ACCOMMODATION {distance: '2.5km'}]->(ac)
            """)
            session.run("""
                MATCH (a:Attraction {name: '浮山风景区'}), (ac:Accommodation {name: '铜陵永泉农庄度假村'})
                CREATE (a)-[:NEAR_ACCOMMODATION {distance: '5km', note: '近火山地貌景区'}]->(ac)
            """)
            session.run("""
                MATCH (c:City {name: '铜陵'}), (t:Transportation)
                WHERE t.name IN ['铜陵站', '铜陵公交']
                CREATE (c)-[:HAS_TRANSPORTATION]->(t)
            """)
            session.run("""
                MATCH (a:Attraction {name: '浮山风景区'})
                SET a.features = '以火山地貌和摩崖石刻为特色，被誉为"中国第一文山"'
            """)

        print("铜陵旅游数据导入完成！")

    def import_anqing_data(self):
        """导入安庆旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
                CREATE 
                (aq:City {name: '安庆', level: '四线城市', description: '黄梅戏乡，安徽故省会，文化之邦'})
            """)

            # 2. 创建景点节点
            session.run("""
                CREATE 
                (tianzhushan:Attraction {name: '天柱山', type: '自然景观', rating: 4.7, opening_hours: '7:00-17:30'}),
                (yingjiangsi:Attraction {name: '迎江寺·振风塔', type: '人文景观', rating: 4.5, opening_hours: '8:00-17:30'})
            """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
                CREATE 
                (jiangmaoshuijiao:Food {name: '江毛水饺', type: '地方小吃', price_range: '低', description: '皮薄馅嫩，汤味鲜美'}),
                (shanfenyuanzi:Food {name: '山粉圆子烧肉', type: '地方菜', price_range: '中', description: '圆子Q弹，咸香可口'}),

                (baijinguoj:Accommodation {name: '安庆栢景国际酒店', type: '五星级酒店', price_range: '中高', rating: 4.5}),
                (yingbinguan:Accommodation {name: '安庆迎宾馆', type: '豪华型酒店', price_range: '中', rating: 4.4}),

                (anqingzhan:Transportation {name: '安庆站', type: '火车站', route: '合九铁路、宁安高铁', price: '按里程计费'}),
                (anqinggj:Transportation {name: '安庆公交', type: '公交', route: '覆盖全市', price: '1-2元'})
            """)

            # 4. 创建关系：景点→城市
            session.run("""
                MATCH (a:Attraction), (c:City {name: '安庆'})
                WHERE a.name IN ['天柱山', '迎江寺·振风塔']
                CREATE (a)-[:LOCATED_IN]->(c)
            """)

            # 5. 创建关系：城市→推荐美食
            session.run("""
                MATCH (c:City {name: '安庆'}), (f:Food)
                WHERE f.name IN ['江毛水饺', '山粉圆子烧肉']
                CREATE (c)-[:RECOMMENDS_FOOD]->(f)
            """)

            # 6. 创建关系：景点→附近美食
            session.run("""
                MATCH (a:Attraction {name: '迎江寺·振风塔'}), (f:Food)
                WHERE f.name IN ['江毛水饺', '山粉圆子烧肉']
                CREATE (a)-[:NEAR_FOOD {distance: '1.2km'}]->(f)
            """)
            session.run("""
                MATCH (a:Attraction {name: '天柱山'}), (f:Food {name: '山粉圆子烧肉'})
                CREATE (a)-[:NEAR_FOOD {distance: '5km'}]->(f)
            """)

            # 7. 创建关系：景点→附近住宿、城市→交通及文化特色
            session.run("""
                MATCH (a:Attraction {name: '迎江寺·振风塔'}), (ac:Accommodation {name: '安庆迎宾馆'})
                CREATE (a)-[:NEAR_ACCOMMODATION {distance: '1.5km'}]->(ac)
            """)
            session.run("""
                MATCH (a:Attraction {name: '天柱山'}), (ac:Accommodation {name: '安庆栢景国际酒店'})
                CREATE (a)-[:NEAR_ACCOMMODATION {distance: '20km'}]->(ac)
            """)
            session.run("""
                MATCH (c:City {name: '安庆'}), (t:Transportation)
                WHERE t.name IN ['安庆站', '安庆公交']
                CREATE (c)-[:HAS_TRANSPORTATION]->(t)
            """)
            # 补充黄梅戏文化特色关联
            session.run("""
                MATCH (c:City {name: '安庆'})
                CREATE (c)-[:FEATURES_CULTURE {type: '黄梅戏', description: '可欣赏正宗黄梅戏表演'}]->(:Cultural {name: '黄梅戏艺术'})
            """)

        print("安庆旅游数据导入完成！")

    def import_huangshan_data(self):
        """导入黄山旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
                CREATE 
                (hs:City {name: '黄山', level: '四线城市', description: '世界自然与文化双遗产地，徽文化发祥地'})
            """)

            # 2. 创建景点节点
            session.run("""
                CREATE 
                (huangshanfengjing:Attraction {name: '黄山风景区', type: '自然景观', rating: 4.9, opening_hours: '全天开放，索道时间不一'}),
                (hongcun:Attraction {name: '宏村', type: '人文景观', rating: 4.7, opening_hours: '全天开放'})
            """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
                CREATE 
                (chouguiyu:Food {name: '臭鳜鱼', type: '徽菜', price_range: '中高', description: '闻着臭，吃着香，肉质鲜嫩'}),
                (maodoufu:Food {name: '毛豆腐', type: '徽菜/小吃', price_range: '中低', description: '口感独特，风味醇厚'}),

                (yuerongzhuang:Accommodation {name: '黄山悦榕庄', type: '豪华度假村', price_range: '高', rating: 4.8}),
                (guojidajiudian:Accommodation {name: '黄山国际大酒店', type: '五星级酒店', price_range: '中高', rating: 4.5}),

                (huangshanbeizhan:Transportation {name: '黄山北站', type: '高铁站', route: '合福高铁、杭黄高铁', price: '按里程计费'}),
                (keyunzhongxin:Transportation {name: '黄山旅游客运中心', type: '大巴', route: '连接景区与市区/高铁站', price: '按路线计费'})
            """)

            # 4. 创建关系：景点→城市
            session.run("""
                MATCH (a:Attraction), (c:City {name: '黄山'})
                WHERE a.name IN ['黄山风景区', '宏村']
                CREATE (a)-[:LOCATED_IN]->(c)
            """)

            # 5. 创建关系：城市→推荐美食
            session.run("""
                MATCH (c:City {name: '黄山'}), (f:Food)
                WHERE f.name IN ['臭鳜鱼', '毛豆腐']
                CREATE (c)-[:RECOMMENDS_FOOD]->(f)
            """)

            # 6. 创建关系：景点→附近美食
            session.run("""
                MATCH (a:Attraction {name: '宏村'}), (f:Food)
                WHERE f.name IN ['臭鳜鱼', '毛豆腐']
                CREATE (a)-[:NEAR_FOOD {distance: '1km'}]->(f)
            """)
            session.run("""
                MATCH (a:Attraction {name: '黄山风景区'}), (f:Food {name: '毛豆腐'})
                CREATE (a)-[:NEAR_FOOD {distance: '3km'}]->(f)
            """)

            # 7. 创建关系：景点→附近住宿、城市→交通及旅游提示
            session.run("""
                MATCH (a:Attraction {name: '黄山风景区'}), (ac:Accommodation {name: '黄山悦榕庄'})
                CREATE (a)-[:NEAR_ACCOMMODATION {distance: '5km', note: '建议提前预订以观赏日出'}]->(ac)
            """)
            session.run("""
                MATCH (a:Attraction {name: '宏村'}), (ac:Accommodation {name: '黄山国际大酒店'})
                CREATE (a)-[:NEAR_ACCOMMODATION {distance: '15km'}]->(ac)
            """)
            session.run("""
                MATCH (c:City {name: '黄山'}), (t:Transportation)
                WHERE t.name IN ['黄山北站', '黄山旅游客运中心']
                CREATE (c)-[:HAS_TRANSPORTATION]->(t)
            """)
            # 交通换乘关系
            session.run("""
                MATCH (t1:Transportation {name: '黄山北站'}), (t2:Transportation {name: '黄山旅游客运中心'})
                CREATE (t1)-[:CONNECTED_TO {description: '无缝衔接景区大巴'}]->(t2)
            """)

        print("黄山旅游数据导入完成！")

    def import_chuzhou_data(self):
        """导入滁州旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
                CREATE 
                (cz:City {name: '滁州', level: '四线城市', description: '皖东门户，南京都市圈核心城市，欧阳修故地'})
            """)

            # 2. 创建景点节点
            session.run("""
                CREATE 
                (langyashan:Attraction {name: '琅琊山风景区', type: '自然+人文景观', rating: 4.6, opening_hours: '8:00-17:30'}),
                (xiaogangcun:Attraction {name: '小岗村', type: '人文景观', rating: 4.3, opening_hours: '全天开放'})
            """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
                CREATE 
                (langyasusugar:Food {name: '琅琊酥糖', type: '地方特产', price_range: '低', description: '香甜酥脆，入口即化'}),
                (guanbaniu:Food {name: '管坝牛肉', type: '地方菜', price_range: '中', description: '肉质紧实，卤香浓郁'}),

                (kaidihu:Accommodation {name: '滁州凯迪温德姆至尊豪廷大酒店', type: '五星级酒店', price_range: '中高', rating: 4.5}),
                (jinpeng:Accommodation {name: '滁州金鹏广场酒店', type: '豪华型酒店', price_range: '中', rating: 4.3}),

                (chuzhouzhan:Transportation {name: '滁州站', type: '高铁站', route: '京沪高铁沿线', price: '按里程计费'}),
                (chuzhoubeizhan:Transportation {name: '滁州北站', type: '火车站', route: '京沪铁路沿线', price: '按里程计费'})
            """)

            # 4. 创建关系：景点→城市
            session.run("""
                MATCH (a:Attraction), (c:City {name: '滁州'})
                WHERE a.name IN ['琅琊山风景区', '小岗村']
                CREATE (a)-[:LOCATED_IN]->(c)
            """)

            # 5. 创建关系：城市→推荐美食
            session.run("""
                MATCH (c:City {name: '滁州'}), (f:Food)
                WHERE f.name IN ['琅琊酥糖', '管坝牛肉']
                CREATE (c)-[:RECOMMENDS_FOOD]->(f)
            """)

            # 6. 创建关系：景点→附近美食
            session.run("""
                MATCH (a:Attraction {name: '琅琊山风景区'}), (f:Food {name: '琅琊酥糖'})
                CREATE (a)-[:NEAR_FOOD {distance: '1km', note: '景区特色伴手礼'}]->(f)
            """)
            session.run("""
                MATCH (a:Attraction {name: '小岗村'}), (f:Food {name: '管坝牛肉'})
                CREATE (a)-[:NEAR_FOOD {distance: '4km'}]->(f)
            """)

            # 7. 创建关系：景点→附近住宿、城市→交通及文化关联
            session.run("""
                MATCH (a:Attraction {name: '琅琊山风景区'}), (ac:Accommodation {name: '滁州金鹏广场酒店'})
                CREATE (a)-[:NEAR_ACCOMMODATION {distance: '3km'}]->(ac)
            """)
            session.run("""
                MATCH (a:Attraction {name: '小岗村'}), (ac:Accommodation {name: '滁州凯迪温德姆至尊豪廷大酒店'})
                CREATE (a)-[:NEAR_ACCOMMODATION {distance: '25km'}]->(ac)
            """)
            session.run("""
                MATCH (c:City {name: '滁州'}), (t:Transportation)
                WHERE t.name IN ['滁州站', '滁州北站']
                CREATE (c)-[:HAS_TRANSPORTATION]->(t)
            """)
            # 补充琅琊山文化背景关联
            session.run("""
                MATCH (a:Attraction {name: '琅琊山风景区'})
                SET a.cultural_background = '因欧阳修《醉翁亭记》闻名天下'
            """)

        print("滁州旅游数据导入完成！")

    def import_fuyang_data(self):
        """导入阜阳旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
                CREATE 
                (fy:City {name: '阜阳', level: '四线城市', description: '皖北中心城市，百亿江淮粮仓'})
            """)

            # 2. 创建景点节点
            session.run("""
                CREATE 
                (balihe:Attraction {name: '八里河风景区', type: '自然+人文景观', rating: 4.6, opening_hours: '8:00-17:30'}),
                (shengtaiyuan:Attraction {name: '生态园', type: '自然景观', rating: 4.4, opening_hours: '全天开放'})
            """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
                CREATE 
                (gelatiao:Food {name: '格拉条', type: '地方小吃', price_range: '低', description: '面条粗硬，麻酱香浓'}),
                (zhentoumo:Food {name: '枕头馍', type: '地方小吃', price_range: '低', description: '形似枕头，松软耐存'}),

                (wandajiahua:Accommodation {name: '阜阳万达嘉华酒店', type: '五星级酒店', price_range: '中高', rating: 4.5}),
                (baolongwendemu:Accommodation {name: '阜阳宝龙温德姆至尊豪廷大酒店', type: '五星级酒店', price_range: '中高', rating: 4.4}),

                (fuyangxizhan:Transportation {name: '阜阳西站', type: '高铁站', route: '商合杭高铁、郑阜高铁', price: '按里程计费'}),
                (fuyanggj:Transportation {name: '阜阳公交', type: '公交', route: '覆盖全市', price: '1-2元'})
            """)

            # 4. 创建关系：景点→城市
            session.run("""
                MATCH (a:Attraction), (c:City {name: '阜阳'})
                WHERE a.name IN ['八里河风景区', '生态园']
                CREATE (a)-[:LOCATED_IN]->(c)
            """)

            # 5. 创建关系：城市→推荐美食
            session.run("""
                MATCH (c:City {name: '阜阳'}), (f:Food)
                WHERE f.name IN ['格拉条', '枕头馍']
                CREATE (c)-[:RECOMMENDS_FOOD]->(f)
            """)

            # 6. 创建关系：景点→附近美食
            session.run("""
                MATCH (a:Attraction {name: '生态园'}), (f:Food)
                WHERE f.name IN ['格拉条', '枕头馍']
                CREATE (a)-[:NEAR_FOOD {distance: '2km'}]->(f)
            """)
            session.run("""
                MATCH (a:Attraction {name: '八里河风景区'}), (f:Food {name: '格拉条'})
                CREATE (a)-[:NEAR_FOOD {distance: '8km'}]->(f)
            """)

            # 7. 创建关系：景点→附近住宿、城市→交通及景区等级
            session.run("""
                MATCH (a:Attraction {name: '八里河风景区'}), (ac:Accommodation {name: '阜阳万达嘉华酒店'})
                CREATE (a)-[:NEAR_ACCOMMODATION {distance: '10km', note: '国家级AAAAA旅游景区'}]->(ac)
            """)
            session.run("""
                MATCH (a:Attraction {name: '生态园'}), (ac:Accommodation {name: '阜阳宝龙温德姆至尊豪廷大酒店'})
                CREATE (a)-[:NEAR_ACCOMMODATION {distance: '3km'}]->(ac)
            """)
            session.run("""
                MATCH (c:City {name: '阜阳'}), (t:Transportation)
                WHERE t.name IN ['阜阳西站', '阜阳公交']
                CREATE (c)-[:HAS_TRANSPORTATION]->(t)
            """)
            # 补充八里河风景区等级属性
            session.run("""
                MATCH (a:Attraction {name: '八里河风景区'})
                SET a.level = '国家级AAAAA旅游景区'
            """)

        print("阜阳旅游数据导入完成！")

    def import_suzhou_data(self):
        """导入宿州旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
                CREATE 
                (sz:City {name: '宿州', level: '四线城市', description: '中国云都，泗水古郡，马戏之乡'})
            """)

            # 2. 创建景点节点
            session.run("""
                CREATE 
                (huangcangyu:Attraction {name: '皇藏峪国家森林公园', type: '自然景观', rating: 4.5, opening_hours: '8:30-17:00'}),
                (xinbianhe:Attraction {name: '宿州新汴河风景区', type: '自然+人文景观', rating: 4.3, opening_hours: '全天开放'})
            """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
                CREATE 
                (fulijishaoji:Food {name: '符离集烧鸡', type: '地方名菜', price_range: '中', description: '肉烂脱骨，肥而不腻'}),
                (satang:Food {name: 'SA汤', type: '地方小吃', price_range: '低', description: '用鸡汤熬制，鲜香辛辣'}),

                (fengdaguoji:Accommodation {name: '宿州丰大国际大酒店', type: '五星级酒店', price_range: '中高', rating: 4.4}),
                (suzhouguoji:Accommodation {name: '宿州国际大酒店', type: '豪华型酒店', price_range: '中', rating: 4.2}),

                (suzhoudongzhan:Transportation {name: '宿州东站', type: '高铁站', route: '京沪高铁沿线', price: '按里程计费'}),
                (suzhougj:Transportation {name: '宿州公交', type: '公交', route: '覆盖全市', price: '1-2元'})
            """)

            # 4. 创建关系：景点→城市
            session.run("""
                MATCH (a:Attraction), (c:City {name: '宿州'})
                WHERE a.name IN ['皇藏峪国家森林公园', '宿州新汴河风景区']
                CREATE (a)-[:LOCATED_IN]->(c)
            """)

            # 5. 创建关系：城市→推荐美食
            session.run("""
                MATCH (c:City {name: '宿州'}), (f:Food)
                WHERE f.name IN ['符离集烧鸡', 'SA汤']
                CREATE (c)-[:RECOMMENDS_FOOD]->(f)
            """)

            # 6. 创建关系：景点→附近美食
            session.run("""
                MATCH (a:Attraction {name: '宿州新汴河风景区'}), (f:Food)
                WHERE f.name IN ['符离集烧鸡', 'SA汤']
                CREATE (a)-[:NEAR_FOOD {distance: '1.5km'}]->(f)
            """)
            session.run("""
                MATCH (a:Attraction {name: '皇藏峪国家森林公园'}), (f:Food {name: '符离集烧鸡'})
                CREATE (a)-[:NEAR_FOOD {distance: '7km'}]->(f)
            """)

            # 7. 创建关系：景点→附近住宿、城市→交通及美食特色
            session.run("""
                MATCH (a:Attraction {name: '皇藏峪国家森林公园'}), (ac:Accommodation {name: '宿州丰大国际大酒店'})
                CREATE (a)-[:NEAR_ACCOMMODATION {distance: '12km'}]->(ac)
            """)
            session.run("""
                MATCH (a:Attraction {name: '宿州新汴河风景区'}), (ac:Accommodation {name: '宿州国际大酒店'})
                CREATE (a)-[:NEAR_ACCOMMODATION {distance: '2km'}]->(ac)
            """)
            session.run("""
                MATCH (c:City {name: '宿州'}), (t:Transportation)
                WHERE t.name IN ['宿州东站', '宿州公交']
                CREATE (c)-[:HAS_TRANSPORTATION]->(t)
            """)
            # 补充符离集烧鸡的荣誉属性
            session.run("""
                MATCH (f:Food {name: '符离集烧鸡'})
                SET f.honor = '中国四大名鸡之一'
            """)

        print("宿州旅游数据导入完成！")

    def import_liuan_data(self):
        """导入六安安旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
                CREATE 
                (la:City {name: '六安', level: '四线线城市', description: '皖西名城，将军故里，六安瓜片原产地'})
            """)

            # 2. 创建景点节点
            session.run("""
                CREATE 
                (tiantangzhai:Attraction {name: '天堂寨风景区', type: '自然景观', rating: 4.7, opening_hours: '7:30-17:30'}),
                (wanfohu:Attraction {name: '万佛湖风景区', type: '自然景观', rating: 4.6, opening_hours: '8:00-17:30'})
            """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
                CREATE 
                (liuanjiangya:Food {name: '六安酱鸭', type: '地方菜', price_range: '中', description: '色泽酱红，香醇味厚'}),
                (haoziBaba:Food {name: '蒿子粑粑', type: '地方小吃', price_range: '低', description: '外皮酥脆，清香扑鼻'}),

                (shuguangbozun:Accommodation {name: '六安曙光铂尊酒店', type: '豪华型酒店', price_range: '中', rating: 4.4}),
                (suoyijunlan:Accommodation {name: '六安索伊君澜大酒店', type: '豪华型酒店', price_range: '中', rating: 4.3}),

                (liuanzhan:Transportation {name: '六安站', type: '高铁站', route: '宁西铁路、合武高铁', price: '按里程计费'}),
                (liuangj:Transportation {name: '六安公交', type: '公交', route: '覆盖全市', price: '1-2元'})
            """)

            # 4. 创建关系：景点→城市
            session.run("""
                MATCH (a:Attraction), (c:City {name: '六安'})
                WHERE a.name IN ['天堂寨风景区', '万佛湖风景区']
                CREATE (a)-[:LOCATED_IN]->(c)
            """)

            # 5. 创建关系：城市→推荐美食
            session.run("""
                MATCH (c:City {name: '六安'}), (f:Food)
                WHERE f.name IN ['六安酱鸭', '蒿子粑粑']
                CREATE (c)-[:RECOMMENDS_FOOD]->(f)
            """)

            # 6. 创建关系：景点→附近美食
            session.run("""
                MATCH (a:Attraction {name: '万佛湖风景区'}), (f:Food)
                WHERE f.name IN ['六安酱鸭', '蒿子粑粑']
                CREATE (a)-[:NEAR_FOOD {distance: '3km'}]->(f)
            """)
            session.run("""
                MATCH (a:Attraction {name: '天堂寨风景区'}), (f:Food {name: '蒿子粑粑'})
                CREATE (a)-[:NEAR_FOOD {distance: '5km'}]->(f)
            """)

            # 7. 创建关系：景点→附近住宿、城市→交通及特产关联
            session.run("""
                MATCH (a:Attraction {name: '天堂寨风景区'}), (ac:Accommodation {name: '六安曙光铂尊酒店'})
                CREATE (a)-[:NEAR_ACCOMMODATION {distance: '30km'}]->(ac)
            """)
            session.run("""
                MATCH (a:Attraction {name: '万佛湖风景区'}), (ac:Accommodation {name: '六安索伊君澜大酒店'})
                CREATE (a)-[:NEAR_ACCOMMODATION {distance: '25km'}]->(ac)
            """)
            session.run("""
                MATCH (c:City {name: '六安'}), (t:Transportation)
                WHERE t.name IN ['六安站', '六安公交']
                CREATE (c)-[:HAS_TRANSPORTATION]->(t)
            """)
            # 补充六安瓜片特产关联
            session.run("""
                MATCH (c:City {name: '六安'})
                CREATE (c)-[:HAS_SPECIALTY {type: '绿茶', description: '著名绿茶"六安瓜片"原产地'}]->(:Specialty {name: '六安瓜片'})
            """)

        print("六安旅游数据导入完成！")

    def import_bozhou_data(self):
        """导入亳州旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
                CREATE 
                (bz:City {name: '亳州', level: '四线城市', description: '中华药都，曹操华佗故里，国家历史文化名城'})
            """)

            # 2. 创建景点节点
            session.run("""
                CREATE 
                (huaxilou:Attraction {name: '花戏楼', type: '人文景观', rating: 4.5, opening_hours: '8:30-17:30'}),
                (caocaoyunbingdao:Attraction {name: '曹操运兵道', type: '人文景观', rating: 4.4, opening_hours: '8:30-17:30'})
            """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
                CREATE 
                (niuroumo:Food {name: '牛肉馍', type: '地方小吃', price_range: '低', description: '皮脆馅香，饱腹感强'}),
                (guoyanggankou:Food {name: '涡阳干扣面', type: '地方小吃', price_range: '低', description: '面条爽滑，辣中带香'}),

                (bozhoubinguan:Accommodation {name: '亳州宾馆', type: '豪华型酒店', price_range: '中', rating: 4.3}),
                (bozhouwandajiahua:Accommodation {name: '亳州万达嘉华酒店', type: '五星级酒店', price_range: '中高', rating: 4.5}),

                (bozhounanzhan:Transportation {name: '亳州南站', type: '高铁站', route: '商合杭高铁沿线', price: '按里程计费'}),
                (bozhougj:Transportation {name: '亳州公交', type: '公交', route: '覆盖全市', price: '1-2元'})
            """)

            # 4. 创建关系：景点→城市
            session.run("""
                MATCH (a:Attraction), (c:City {name: '亳州'})
                WHERE a.name IN ['花戏楼', '曹操运兵道']
                CREATE (a)-[:LOCATED_IN]->(c)
            """)

            # 5. 创建关系：城市→推荐美食
            session.run("""
                MATCH (c:City {name: '亳州'}), (f:Food)
                WHERE f.name IN ['牛肉馍', '涡阳干扣面']
                CREATE (c)-[:RECOMMENDS_FOOD]->(f)
            """)

            # 6. 创建关系：景点→附近美食
            session.run("""
                MATCH (a:Attraction {name: '花戏楼'}), (f:Food)
                WHERE f.name IN ['牛肉馍', '涡阳干扣面']
                CREATE (a)-[:NEAR_FOOD {distance: '1km'}]->(f)
            """)
            session.run("""
                MATCH (a:Attraction {name: '曹操运兵道'}), (f:Food {name: '牛肉馍'})
                CREATE (a)-[:NEAR_FOOD {distance: '0.8km'}]->(f)
            """)

            # 7. 创建关系：景点→附近住宿、城市→交通及药都特色
            session.run("""
                MATCH (a:Attraction {name: '花戏楼'}), (ac:Accommodation {name: '亳州宾馆'})
                CREATE (a)-[:NEAR_ACCOMMODATION {distance: '1.2km'}]->(ac)
            """)
            session.run("""
                MATCH (a:Attraction {name: '曹操运兵道'}), (ac:Accommodation {name: '亳州万达嘉华酒店'})
                CREATE (a)-[:NEAR_ACCOMMODATION {distance: '2km'}]->(ac)
            """)
            session.run("""
                MATCH (c:City {name: '亳州'}), (t:Transportation)
                WHERE t.name IN ['亳州南站', '亳州公交']
                CREATE (c)-[:HAS_TRANSPORTATION]->(t)
            """)
            # 补充药都产业特色关联
            session.run("""
                MATCH (c:City {name: '亳州'})
                CREATE (c)-[:INDUSTRY_FEATURE {title: '中华药都', description: '中国四大药都之首，拥有全国最大的中药材交易中心'}]->(:Industry {name: '中药材产业'})
            """)

        print("亳州旅游数据导入完成！")

    def import_chizhou_data(self):
        """导入导入池州旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
                CREATE 
                (czs:City {name: '池州', level: '五线城市', description: '千载诗人地，中国佛教四大名山之一九华山所在地'})
            """)

            # 2. 创建景点节点
            session.run("""
                CREATE 
                (jiuhuashan:Attraction {name: '九华山风景区', type: '自然+人文景观', rating: 4.8, opening_hours: '全天开放'}),
                (xinghuacun:Attraction {name: '杏花村', type: '人文景观', rating: 4.3, opening_hours: '8:30-17:00'})
            """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
                CREATE 
                (jiuhuaszhaizhai:Food {name: '九华素斋', type: '地方特色', price_range: '中', description: '选料精细，风味清新'}),
                (chizhouxiaba:Food {name: '池州小巴', type: '地方菜', price_range: '中', description: '鱼肉鲜嫩，汤汁奶白'}),

                (pingtianbandao:Accommodation {name: '池州平天半岛大酒店', type: '豪华型酒店', price_range: '中', rating: 4.5}),
                (jiuhuashanjulong:Accommodation {name: '九华山聚龙大酒店', type: '豪华型酒店', price_range: '中', rating: 4.4}),

                (chizhouzhan:Transportation {name: '池州站', type: '高铁站', route: '宁安高铁沿线', price: '按里程计费'}),
                (jiuhuakeyun:Transportation {name: '九华山旅游客运中心', type: '大巴', route: '连接景区与市区/高铁站', price: '按路线计费'})
            """)

            # 4. 创建关系：景点→城市
            session.run("""
                MATCH (a:Attraction), (c:City {name: '池州'})
                WHERE a.name IN ['九华山风景区', '杏花村']
                CREATE (a)-[:LOCATED_IN]->(c)
            """)

            # 5. 创建关系：城市→推荐美食
            session.run("""
                MATCH (c:City {name: '池州'}), (f:Food)
                WHERE f.name IN ['九华素斋', '池州小巴']
                CREATE (c)-[:RECOMMENDS_FOOD]->(f)
            """)

            # 6. 创建关系：景点→附近美食
            session.run("""
                MATCH (a:Attraction {name: '九华山风景区'}), (f:Food {name: '九华素斋'})
                CREATE (a)-[:NEAR_FOOD {distance: '1km', note: '景区特色餐饮'}]->(f)
            """)
            session.run("""
                MATCH (a:Attraction {name: '杏花村'}), (f:Food {name: '池州小巴'})
                CREATE (a)-[:NEAR_FOOD {distance: '2km'}]->(f)
            """)

            # 7. 创建关系：景点→附近住宿、城市→交通及宗教特色
            session.run("""
                MATCH (a:Attraction {name: '九华山风景区'}), (ac:Accommodation {name: '九华山聚龙大酒店'})
                CREATE (a)-[:NEAR_ACCOMMODATION {distance: '3km', note: '近核心景区'}]->(ac)
            """)
            session.run("""
                MATCH (a:Attraction {name: '杏花村'}), (ac:Accommodation {name: '池州平天半岛大酒店'})
                CREATE (a)-[:NEAR_ACCOMMODATION {distance: '4km'}]->(ac)
            """)
            session.run("""
                MATCH (c:City {name: '池州'}), (t:Transportation)
                WHERE t.name IN ['池州站', '九华山旅游客运中心']
                CREATE (c)-[:HAS_TRANSPORTATION]->(t)
            """)
            # 交通换乘关系
            session.run("""
                MATCH (t1:Transportation {name: '池州站'}), (t2:Transportation {name: '九华山旅游客运中心'})
                CREATE (t1)-[:CONNECTED_TO {frequency: '每30分钟一班'}]->(t2)
            """)
            # 补充九华山宗教属性
            session.run("""
                MATCH (a:Attraction {name: '九华山风景区'})
                SET a.religious_attribute = '地藏王菩萨道场，香火鼎盛'
            """)

        print("池州旅游数据导入完成！")

    def import_xuancheng_data(self):
        """导入宣城旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
                CREATE 
                (xc:City {name: '宣城', level: '五线城市', description: '中国文房四宝之乡，山水诗乡'})
            """)

            # 2. 创建景点节点
            session.run("""
                CREATE 
                (taohuatan:Attraction {name: '泾县桃花潭', type: '自然+人文景观', rating: 4.5, opening_hours: '7:30-17:30'}),
                (longchuan:Attraction {name: '绩溪龙川景区', type: '人文景观', rating: 4.6, opening_hours: '8:00-17:00'})
            """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
                CREATE 
                (hushiypg:Food {name: '胡适一品锅', type: '徽菜', price_range: '中高', description: '用料丰富，层层堆叠'}),
                (jixichaofans:Food {name: '绩溪炒粉丝', type: '地方菜', price_range: '中低', description: '干香爽滑，配料丰富'}),

                (jingtingshandujia:Accommodation {name: '宣城敬亭山度假村', type: '度假酒店', price_range: '中', rating: 4.3}),
                (xuanchengbinguan:Accommodation {name: '宣城宾馆', type: '豪华型酒店', price_range: '中', rating: 4.2}),

                (xuanchengzhan:Transportation {name: '宣城站', type: '高铁站', route: '商合杭高铁沿线', price: '按里程计费'}),
                (xuanchenggj:Transportation {name: '宣城公交', type: '公交', route: '覆盖全市', price: '1-2元'})
            """)

            # 4. 创建关系：景点→城市
            session.run("""
                MATCH (a:Attraction), (c:City {name: '宣城'})
                WHERE a.name IN ['泾县桃花潭', '绩溪龙川景区']
                CREATE (a)-[:LOCATED_IN]->(c)
            """)

            # 5. 创建关系：城市→推荐美食
            session.run("""
                MATCH (c:City {name: '宣城'}), (f:Food)
                WHERE f.name IN ['胡适一品锅', '绩溪炒粉丝']
                CREATE (c)-[:RECOMMENDS_FOOD]->(f)
            """)

            # 6. 创建关系：景点→附近美食
            session.run("""
                MATCH (a:Attraction {name: '绩溪龙川景区'}), (f:Food {name: '绩溪炒粉丝'})
                CREATE (a)-[:NEAR_FOOD {distance: '1km', note: '当地特色美食'}]->(f)
            """)
            session.run("""
                MATCH (a:Attraction {name: '泾县桃花潭'}), (f:Food {name: '胡适一品锅'})
                CREATE (a)-[:NEAR_FOOD {distance: '4km'}]->(f)
            """)

            # 7. 创建关系：景点→附近住宿、城市→交通及文房四宝特色
            session.run("""
                MATCH (a:Attraction {name: '泾县桃花潭'}), (ac:Accommodation {name: '宣城敬亭山度假村'})
                CREATE (a)-[:NEAR_ACCOMMODATION {distance: '20km'}]->(ac)
            """)
            session.run("""
                MATCH (a:Attraction {name: '绩溪龙川景区'}), (ac:Accommodation {name: '宣城宾馆'})
                CREATE (a)-[:NEAR_ACCOMMODATION {distance: '35km'}]->(ac)
            """)
            session.run("""
                MATCH (c:City {name: '宣城'}), (t:Transportation)
                WHERE t.name IN ['宣城站', '宣城公交']
                CREATE (c)-[:HAS_TRANSPORTATION]->(t)
            """)
            # 补充文房四宝特产关联
            session.run("""
                MATCH (c:City {name: '宣城'})
                CREATE (c)-[:HAS_CULTURAL_RELIC {category: '文房四宝', description: '宣纸、宣笔、徽墨原产地'}]->(:CulturalRelic {name: '宣城文房四宝'})
            """)

        print("宣城旅游数据导入完成！")

    def import_chaohu_data(self):

        """导入巢湖市旅游数据"""
        with self.driver.session() as session:
         session.run("""
            CREATE 
            (ch:City {
                name: '巢湖', 
                level: '县级市（由合肥市代管）', 
                description: '环湖宜居城市，鱼米之乡，周瑜故里'
            })
        """)

        # 2. 创建景点节点
         session.run("""
            CREATE 
            (laoshandao:Attraction {
                name: '姥山岛', 
                type: '自然景观', 
                rating: 4.5, 
                opening_hours: '8:30 - 17:00'
            }),
            (ziweidong:Attraction {
                name: '紫微洞', 
                type: '自然景观', 
                rating: 4.3, 
                opening_hours: '8:00 - 17:00'
            })
        """)

        # 3. 创建美食、住宿、交通节点
         session.run("""
            CREATE 
            (chaohuyinyu:Food {
                name: '巢湖银鱼', 
                type: '地方菜', 
                price_range: '中', 
                description: '肉质细腻，味道鲜美'
            }),
            (dongguanlaoetang:Food {
                name: '东关老鹅汤', 
                type: '地方菜', 
                price_range: '中', 
                description: '汤色醇厚，香气扑鼻'
            }),

            (shenyehotspring:Accommodation {
                name: '巢湖深业温泉酒店', 
                type: '度假酒店', 
                price_range: '中', 
                rating: 4.4
            }),
            (chaohuguojidian:Accommodation {
                name: '巢湖国际饭店', 
                type: '高档型酒店', 
                price_range: '中', 
                rating: 4.2
            }),

            (hechaochengji:Transportation {
                name: '合巢城际铁路', 
                type: '高铁', 
                route: '合肥南站 - 巢湖东站', 
                price: '10-20元'
            }),
            (chaohugj:Transportation {
                name: '巢湖公交', 
                type: '公交', 
                route: '覆盖主城区', 
                price: '1-2元'
            })
        """)

        # 4. 创建关系：景点→城市
         session.run("""
            MATCH (a:Attraction), (c:City {name: '巢湖'})
            WHERE a.name IN ['姥山岛', '紫微洞']
            CREATE (a)-[:LOCATED_IN]->(c)
        """)

        # 5. 创建关系：城市→推荐美食
         session.run("""
            MATCH (c:City {name: '巢湖'}), (f:Food)
            WHERE f.name IN ['巢湖银鱼', '东关老鹅汤']
            CREATE (c)-[:RECOMMENDS_FOOD]->(f)
        """)

        # 6. 创建关系：景点→附近美食（突出湖鲜特色）
         session.run("""
            MATCH (a:Attraction {name: '姥山岛'}), (f:Food {name: '巢湖银鱼'})
            CREATE (a)-[:NEAR_FOOD {distance: '0.5km', note: '岛上可品尝新鲜湖鲜'}]->(f)
        """)
         session.run("""
            MATCH (a:Attraction {name: '紫微洞'}), (f:Food {name: '东关老鹅汤'})
            CREATE (a)-[:NEAR_FOOD {distance: '3km'}]->(f)
        """)

        # 7. 创建关系：景点→附近住宿
         session.run("""
            MATCH (a:Attraction {name: '姥山岛'}), (ac:Accommodation {name: '巢湖深业温泉酒店'})
            CREATE (a)-[:NEAR_ACCOMMODATION {distance: '8km'}]->(ac)
        """)
         session.run("""
            MATCH (a:Attraction {name: '紫微洞'}), (ac:Accommodation {name: '巢湖国际饭店'})
            CREATE (a)-[:NEAR_ACCOMMODATION {distance: '5km'}]->(ac)
        """)

        # 8. 创建关系：城市→交通及代管关系
         session.run("""
            MATCH (c:City {name: '巢湖'}), (t:Transportation)
            WHERE t.name IN ['合巢城际铁路', '巢湖公交']
            CREATE (c)-[:HAS_TRANSPORTATION]->(t)
        """)
        # 与合肥的代管及交通关联
         session.run("""
            MATCH (c1:City {name: '巢湖'}), (c2:City {name: '合肥'})
            CREATE (c1)-[:ADMINISTERED_BY {type: '代管'}]->(c2),
                   (c1)-[:CONNECTED_BY {transport: '合巢城际铁路', duration: '约30分钟'}]->(c2)
        """)

        # 9. 补充姥山岛游览提示
         session.run("""
            MATCH (a:Attraction {name: '姥山岛'})
            SET a.tip = '需乘船往返，可品尝新鲜湖鲜'
        """)

        print("巢湖旅游数据导入完成！")

    def import_wuwei_data(self):
        """导入无为市旅游数据"""
        with self.driver.session() as session:
        # 1. 创建城市节点（标注县级市及代管关系）
         session.run("""
            CREATE 
            (ww:City {
                name: '无为', 
                level: '县级市（由芜湖市代管）', 
                description: '皖江城市，鱼米之乡，劳务之乡'
            })
        """)

        # 2. 创建景点节点
         session.run("""
            CREATE 
            (tianjingshan:Attraction {
                name: '天井山国家森林公园', 
                type: '自然景观', 
                rating: 4.4, 
                opening_hours: '8:00 - 17:00'
            }),
            (huangjinta:Attraction {
                name: '黄金塔', 
                type: '人文景观', 
                rating: 4.2, 
                opening_hours: '全天开放'
            })
        """)

        # 3. 创建美食、住宿、交通节点
         session.run("""
            CREATE 
            (wuweibanya:Food {
                name: '无为板鸭（非遗）', 
                type: '地方名菜', 
                price_range: '中低', 
                description: '先熏后卤，金黄油亮，香气浓郁'
            }),
            (yanqiaohuasheng:Food {
                name: '严桥花生米', 
                type: '地方特产', 
                price_range: '低', 
                description: '香脆可口，远近闻名'
            }),

            (wuweibinguan:Accommodation {
                name: '无为宾馆', 
                type: '高档型酒店', 
                price_range: '中', 
                rating: 4.3
            }),
            (wuweitieshan:Accommodation {
                name: '无为铁山宾馆', 
                type: '商务型酒店', 
                price_range: '中低', 
                rating: 4.1
            }),

            (wuweizhan:Transportation {
                name: '无为站', 
                type: '高铁站', 
                route: '京福高铁沿线', 
                price: '按里程计费'
            }),
            (wuweigj:Transportation {
                name: '无为公交', 
                type: '公交', 
                route: '覆盖主城区及乡镇', 
                price: '1-3元'
            })
        """)

        # 4. 创建关系：景点→城市
         session.run("""
            MATCH (a:Attraction), (c:City {name: '无为'})
            WHERE a.name IN ['天井山国家森林公园', '黄金塔']
            CREATE (a)-[:LOCATED_IN]->(c)
        """)

        # 5. 创建关系：城市→推荐美食
         session.run("""
            MATCH (c:City {name: '无为'}), (f:Food)
            WHERE f.name IN ['无为板鸭（非遗）', '严桥花生米']
            CREATE (c)-[:RECOMMENDS_FOOD]->(f)
        """)

        # 6. 创建关系：景点→附近美食（突出地方特色）
         session.run("""
            MATCH (a:Attraction {name: '黄金塔'}), (f:Food {name: '无为板鸭（非遗）'})
            CREATE (a)-[:NEAR_FOOD {distance: '1.5km', note: '发源地特色美食'}]->(f)
        """)
         session.run("""
            MATCH (a:Attraction {name: '天井山国家森林公园'}), (f:Food {name: '严桥花生米'})
            CREATE (a)-[:NEAR_FOOD {distance: '8km', note: '推荐作为伴手礼'}]->(f)
        """)

        # 7. 创建关系：景点→附近住宿
         session.run("""
            MATCH (a:Attraction {name: '天井山国家森林公园'}), (ac:Accommodation {name: '无为宾馆'})
            CREATE (a)-[:NEAR_ACCOMMODATION {distance: '12km'}]->(ac)
        """)
         session.run("""
            MATCH (a:Attraction {name: '黄金塔'}), (ac:Accommodation {name: '无为铁山宾馆'})
            CREATE (a)-[:NEAR_ACCOMMODATION {distance: '2km'}]->(ac)
        """)

        # 8. 创建关系：城市→交通及代管关系
         session.run("""
            MATCH (c:City {name: '无为'}), (t:Transportation)
            WHERE t.name IN ['无为站', '无为公交']
            CREATE (c)-[:HAS_TRANSPORTATION]->(t)
        """)
        # 与芜湖的代管及交通关联
         session.run("""
            MATCH (c1:City {name: '无为'}), (c2:City {name: '芜湖'})
            CREATE (c1)-[:ADMINISTERED_BY {type: '代管'}]->(c2),
                   (c1)-[:CONNECTED_BY {transport: '高铁/公路', note: '交通便捷'}]->(c2)
        """)

        # 9. 补充高铁出行提示
         session.run("""
            MATCH (t:Transportation {name: '无为站'})
            SET t.tip = '可快速抵达合肥、铜陵、黄山等城市'
        """)

        print("无为旅游数据导入完成！")

    def import_tongcheng_data(self):
        """导入桐城市旅游数据"""
        with self.driver.session() as session:
        # 1. 创建城市节点（标注县级市及代管关系）
         session.run("""
            CREATE 
            (tc:City {
                name: '桐城', 
                level: '县级市（由安庆市代管）', 
                description: '江淮文化发源地，桐城派故里，黄梅戏之乡'
            })
        """)

        # 2. 创建景点节点
         session.run("""
            CREATE 
            (kongchenglaojie:Attraction {
                name: '孔城老街', 
                type: '人文景观', 
                rating: 4.4, 
                opening_hours: '8:30 - 17:00'
            }),
            (wenmiaoliuchixiang:Attraction {
                name: '文庙·六尺巷', 
                type: '人文景观', 
                rating: 4.6, 
                opening_hours: '8:30 - 17:30'
            })
        """)

        # 3. 创建美食、住宿、交通节点
         session.run("""
            CREATE 
            (tongchengshuiwan:Food {
                name: '桐城水碗', 
                type: '地方菜', 
                price_range: '中', 
                description: '汤清味醇，非遗技艺'
            }),
            (qingcaoxiangdami:Food {
                name: '青草香大米', 
                type: '地方特产', 
                price_range: '中低', 
                description: '米粒饱满，清香可口'
            }),

            (tongchengguojidajiudian:Accommodation {
                name: '桐城国际大酒店', 
                type: '高档型酒店', 
                price_range: '中', 
                rating: 4.3
            }),
            (tongchengjinruigujing:Accommodation {
                name: '桐城金瑞古井大酒店', 
                type: '商务型酒店', 
                price_range: '中', 
                rating: 4.2
            }),

            (tongchengdongzhan:Transportation {
                name: '桐城东站', 
                type: '高铁站', 
                route: '合安高铁沿线', 
                price: '按里程计费'
            }),
            (tongchenggj:Transportation {
                name: '桐城公交', 
                type: '公交', 
                route: '覆盖主城区', 
                price: '1-2元'
            })
        """)

        # 4. 创建关系：景点→城市
         session.run("""
            MATCH (a:Attraction), (c:City {name: '桐城'})
            WHERE a.name IN ['孔城老街', '文庙·六尺巷']
            CREATE (a)-[:LOCATED_IN]->(c)
        """)

        # 5. 创建关系：城市→推荐美食
         session.run("""
            MATCH (c:City {name: '桐城'}), (f:Food)
            WHERE f.name IN ['桐城水碗', '青草香大米']
            CREATE (c)-[:RECOMMENDS_FOOD]->(f)
        """)

        # 6. 创建关系：景点→附近美食（突出文化与美食关联）
         session.run("""
            MATCH (a:Attraction {name: '文庙·六尺巷'}), (f:Food {name: '桐城水碗'})
            CREATE (a)-[:NEAR_FOOD {distance: '1km', note: '必尝汤菜宴席代表'}]->(f)
        """)
         session.run("""
            MATCH (a:Attraction {name: '孔城老街'}), (f:Food {name: '青草香大米'})
            CREATE (a)-[:NEAR_FOOD {distance: '3km', note: '当地特色农产品'}]->(f)
        """)

        # 7. 创建关系：景点→附近住宿
         session.run("""
            MATCH (a:Attraction {name: '孔城老街'}), (ac:Accommodation {name: '桐城国际大酒店'})
            CREATE (a)-[:NEAR_ACCOMMODATION {distance: '5km'}]->(ac)
        """)
         session.run("""
            MATCH (a:Attraction {name: '文庙·六尺巷'}), (ac:Accommodation {name: '桐城金瑞古井大酒店'})
            CREATE (a)-[:NEAR_ACCOMMODATION {distance: '1.2km'}]->(ac)
        """)

        # 8. 创建关系：城市→交通及代管关系
         session.run("""
            MATCH (c:City {name: '桐城'}), (t:Transportation)
            WHERE t.name IN ['桐城东站', '桐城公交']
            CREATE (c)-[:HAS_TRANSPORTATION]->(t)
        """)
        # 与安庆的代管及交通关联
         session.run("""
            MATCH (c1:City {name: '桐城'}), (c2:City {name: '安庆'})
            CREATE (c1)-[:ADMINISTERED_BY {type: '代管'}]->(c2),
                   (c1)-[:CONNECTED_BY {transport: '合安高铁', duration: '约40分钟'}]->(c2)
        """)

        # 9. 补充六尺巷文化精神提示
         session.run("""
            MATCH (a:Attraction {name: '文庙·六尺巷'})
            SET a.cultural_spirit = '"让他三尺"精神是桐城文化谦让礼信的象征'
        """)

        # 10. 补充高铁站出行提示
         session.run("""
            MATCH (t:Transportation {name: '桐城东站'})
            SET t.tip = '可快速连接合肥与安庆'
        """)

    print("桐城旅游数据导入完成！")

    def import_qianshan_data(self):
        """导入潜山市旅游数据"""
        with self.driver.session() as session:
        # 1. 创建城市节点（标注县级市及代管关系）
         session.run("""
            CREATE 
            (qs:City {
                name: '潜山', 
                level: '县级市（由安庆市代管）', 
                description: '安徽之源，皖国古都，京剧发源地'
            })
        """)

        # 2. 创建景点节点（突出世界地质公园属性）
         session.run("""
            CREATE 
            (tianzhushan:Attraction {
                name: '天柱山风景区', 
                type: '自然景观', 
                rating: 4.8, 
                opening_hours: '7:00 - 17:30',
                honor: '世界地质公园'
            }),
            (shanguliuquan:Attraction {
                name: '山谷流泉文化园', 
                type: '人文景观', 
                rating: 4.4, 
                opening_hours: '8:00 - 17:00'
            })
        """)

        # 3. 创建美食、住宿、交通节点
         session.run("""
            CREATE 
            (tianzhushanshier:Food {
                name: '天柱山石耳', 
                type: '地方特色', 
                price_range: '中高', 
                description: '生长于峭壁，味鲜美，营养高'
            }),
            (xuehugongou:Food {
                name: '雪湖贡藕', 
                type: '地方特产', 
                price_range: '中', 
                description: '口感清脆，藕断丝不连'
            }),

            (liandanhu:Accommodation {
                name: '天柱山炼丹湖度假酒店', 
                type: '度假酒店', 
                price_range: '中高', 
                rating: 4.5
            }),
            (qixiannv:Accommodation {
                name: '潜山七仙女国际大酒店', 
                type: '高档型酒店', 
                price_range: '中', 
                rating: 4.3
            }),

            (qianshanzhan:Transportation {
                name: '潜山站', 
                type: '高铁站', 
                route: '合安高铁沿线', 
                price: '按里程计费'
            }),
            (tianzhushanke:Transportation {
                name: '天柱山旅游客运中心', 
                type: '大巴', 
                route: '连接景区与市区/高铁站', 
                price: '10-20元'
            })
        """)

        # 4. 创建关系：景点→城市
         session.run("""
            MATCH (a:Attraction), (c:City {name: '潜山'})
            WHERE a.name IN ['天柱山风景区', '山谷流泉文化园']
            CREATE (a)-[:LOCATED_IN]->(c)
        """)

        # 5. 创建关系：城市→推荐美食
         session.run("""
            MATCH (c:City {name: '潜山'}), (f:Food)
            WHERE f.name IN ['天柱山石耳', '雪湖贡藕']
            CREATE (c)-[:RECOMMENDS_FOOD]->(f)
        """)

        # 6. 创建关系：景点→附近美食（突出山珍特色）
         session.run("""
            MATCH (a:Attraction {name: '天柱山风景区'}), (f:Food {name: '天柱山石耳'})
            CREATE (a)-[:NEAR_FOOD {distance: '2km', note: '核心山珍特产'}]->(f)
        """)
         session.run("""
            MATCH (a:Attraction {name: '山谷流泉文化园'}), (f:Food {name: '雪湖贡藕'})
            CREATE (a)-[:NEAR_FOOD {distance: '4km', note: '地方特色农产品'}]->(f)
        """)

        # 7. 创建关系：景点→附近住宿
         session.run("""
            MATCH (a:Attraction {name: '天柱山风景区'}), (ac:Accommodation {name: '天柱山炼丹湖度假酒店'})
            CREATE (a)-[:NEAR_ACCOMMODATION {distance: '5km', note: '山顶酒店，方便观日出'}]->(ac)
        """)
         session.run("""
            MATCH (a:Attraction {name: '山谷流泉文化园'}), (ac:Accommodation {name: '潜山七仙女国际大酒店'})
            CREATE (a)-[:NEAR_ACCOMMODATION {distance: '3km'}]->(ac)
        """)

        # 8. 创建关系：城市→交通及代管关系
         session.run("""
            MATCH (c:City {name: '潜山'}), (t:Transportation)
            WHERE t.name IN ['潜山站', '天柱山旅游客运中心']
            CREATE (c)-[:HAS_TRANSPORTATION]->(t)
        """)
        # 与安庆的代管及交通关联
         session.run("""
            MATCH (c1:City {name: '潜山'}), (c2:City {name: '安庆'})
            CREATE (c1)-[:ADMINISTERED_BY {type: '代管'}]->(c2),
                   (c1)-[:CONNECTED_BY {transport: '合安高铁', duration: '约30分钟'}]->(c2)
        """)
        # 交通节点换乘关系
         session.run("""
            MATCH (t1:Transportation {name: '潜山站'}), (t2:Transportation {name: '天柱山旅游客运中心'})
            CREATE (t1)-[:CONNECTED_TO {frequency: '每小时一班'}]->(t2)
        """)

        # 9. 补充天柱山游览提示
         session.run("""
            MATCH (a:Attraction {name: '天柱山风景区'})
            SET a.tip = '面积较大，建议安排一天以上行程，山顶酒店可观赏日出'
        """)

        # 10. 补充高铁站出行提示
         session.run("""
            MATCH (t:Transportation {name: '潜山站'})
            SET t.tip = '可快速抵达合肥、南昌等城市'
        """)

        print("潜山旅游数据导入完成！")

    def import_mingguang_data(self):
        """导入明光市旅游数据"""
        with self.driver.session() as session:
        # 1. 创建城市节点（标注县级市及代管关系）
         session.run("""
            CREATE 
            (mg:City {
                name: '明光', 
                level: '县级市（由滁州市代管）', 
                description: '淮河畔生态城市，明绿豆之乡'
            })
        """)

        # 2. 创建景点节点
         session.run("""
            CREATE 
            (nushanhhu:Attraction {
                name: '女山湖', 
                type: '自然景观', 
                rating: 4.3, 
                opening_hours: '全天开放'
            }),
            (moshan:Attraction {
                name: '抹山', 
                type: '自然+人文景观', 
                rating: 4.2, 
                opening_hours: '8:00 - 17:00'
            })
        """)

        # 3. 创建美食、住宿、交通节点
         session.run("""
            CREATE 
            (nushanhudaxie:Food {
                name: '女山湖大闸蟹', 
                type: '地方特产', 
                price_range: '中', 
                description: '膏满黄肥，味美鲜香'
            }),
            (mingguangludou:Food {
                name: '明光绿豆', 
                type: '地方特产', 
                price_range: '低', 
                description: '皮薄粒大，品质优良'
            }),

            (mingguangkaiyuan:Accommodation {
                name: '明光开元大酒店', 
                type: '高档型酒店', 
                price_range: '中', 
                rating: 4.2
            }),
            (mingguangjiacheng:Accommodation {
                name: '明光嘉城宾馆', 
                type: '商务型酒店', 
                price_range: '中低', 
                rating: 4.0
            }),

            (mingguangzhan:Transportation {
                name: '明光站', 
                type: '火车站', 
                route: '京沪铁路沿线', 
                price: '按里程计费'
            }),
            (mingguanggongjiao:Transportation {
                name: '明光公交', 
                type: '公交', 
                route: '覆盖主城区', 
                price: '1-2元'
            })
        """)

        # 4. 创建关系：景点→城市
         session.run("""
            MATCH (a:Attraction), (c:City {name: '明光'})
            WHERE a.name IN ['女山湖', '抹山']
            CREATE (a)-[:LOCATED_IN]->(c)
        """)

        # 5. 创建关系：城市→推荐美食
         session.run("""
            MATCH (c:City {name: '明光'}), (f:Food)
            WHERE f.name IN ['女山湖大闸蟹', '明光绿豆']
            CREATE (c)-[:RECOMMENDS_FOOD]->(f)
        """)

        # 6. 创建关系：景点→附近美食（突出特产与产地关联）
         session.run("""
            MATCH (a:Attraction {name: '女山湖'}), (f:Food {name: '女山湖大闸蟹'})
            CREATE (a)-[:NEAR_FOOD {distance: '1km', note: '原产地直供，秋季最佳'}]->(f)
        """)
         session.run("""
            MATCH (a:Attraction {name: '抹山'}), (f:Food {name: '明光绿豆'})
            CREATE (a)-[:NEAR_FOOD {distance: '5km', note: '地标性特产'}]->(f)
        """)

        # 7. 创建关系：景点→附近住宿
         session.run("""
            MATCH (a:Attraction {name: '女山湖'}), (ac:Accommodation {name: '明光开元大酒店'})
            CREATE (a)-[:NEAR_ACCOMMODATION {distance: '12km'}]->(ac)
        """)
         session.run("""
            MATCH (a:Attraction {name: '抹山'}), (ac:Accommodation {name: '明光嘉城宾馆'})
            CREATE (a)-[:NEAR_ACCOMMODATION {distance: '8km'}]->(ac)
        """)

        # 8. 创建关系：城市→交通及代管关系
         session.run("""
            MATCH (c:City {name: '明光'}), (t:Transportation)
            WHERE t.name IN ['明光站', '明光公交']
            CREATE (c)-[:HAS_TRANSPORTATION]->(t)
        """)
        # 与滁州的代管及交通关联
         session.run("""
            MATCH (c1:City {name: '明光'}), (c2:City {name: '滁州'})
            CREATE (c1)-[:ADMINISTERED_BY {type: '代管'}]->(c2),
                   (c1)-[:CONNECTED_BY {transport: '京沪铁路', duration: '约1小时'}]->(c2)
        """)

        # 9. 补充抹山历史文化提示
         session.run("""
            MATCH (a:Attraction {name: '抹山'})
            SET a.historical_note = '相传是明代开国皇帝朱元璋的出生地，具有历史文化内涵'
        """)

        # 10. 补充火车站出行提示
         session.run("""
            MATCH (t:Transportation {name: '明光站'})
            SET t.tip = '可乘坐普速列车连接滁州、蚌埠等地'
        """)

        print("明光旅游数据导入完成！")

    def import_jieshou_data(self):
        """导入界首市旅游数据"""
        with self.driver.session() as session:
        # 1. 创建城市节点（标注县级市及代管关系）
         session.run("""
            CREATE 
            (js:City {
                name: '界首', 
                level: '县级市（由阜阳市代管）', 
                description: '皖北门户，小上海，彩陶之乡'
            })
        """)

        # 2. 创建景点节点
         session.run("""
            CREATE 
            (caotiangou:Attraction {
                name: '曹田沟景观带', 
                type: '自然+人文景观', 
                rating: 4.3, 
                opening_hours: '全天开放'
            }),
            (jieshoumuseum:Attraction {
                name: '界首博物馆', 
                type: '人文景观', 
                rating: 4.4, 
                opening_hours: '9:00 - 17:00 (周一闭馆)'
            })
        """)

        # 3. 创建美食、住宿、交通节点
         session.run("""
            CREATE 
            (jieshouniurou:Food {
                name: '界首牛肉', 
                type: '地方小吃', 
                price_range: '中低', 
                description: '肉质紧实，卤香入味'
            }),
            (banji:Food {
                name: '板鸡', 
                type: '地方小吃', 
                price_range: '中低', 
                description: '鸡肉鲜嫩，咸香可口'
            }),

            (fajina:Accommodation {
                name: '界首法姬娜大酒店', 
                type: '高档型酒店', 
                price_range: '中', 
                rating: 4.3
            }),
            (jieshouwendemu:Accommodation {
                name: '界首温德姆酒店', 
                type: '豪华型酒店', 
                price_range: '中高', 
                rating: 4.4
            }),

            (jieshounanzhan:Transportation {
                name: '界首南站', 
                type: '高铁站', 
                route: '郑阜高铁沿线', 
                price: '按里程计费'
            }),
            (jieshougj:Transportation {
                name: '界首公交', 
                type: '公交', 
                route: '覆盖主城区', 
                price: '1-2元'
            })
        """)

        # 4. 创建关系：景点→城市
         session.run("""
            MATCH (a:Attraction), (c:City {name: '界首'})
            WHERE a.name IN ['曹田沟景观带', '界首博物馆']
            CREATE (a)-[:LOCATED_IN]->(c)
        """)

        # 5. 创建关系：城市→推荐美食
         session.run("""
            MATCH (c:City {name: '界首'}), (f:Food)
            WHERE f.name IN ['界首牛肉', '板鸡']
            CREATE (c)-[:RECOMMENDS_FOOD]->(f)
        """)

        # 6. 创建关系：景点→附近美食（突出地方小吃特色）
         session.run("""
            MATCH (a:Attraction {name: '曹田沟景观带'}), (f:Food {name: '界首牛肉'})
            CREATE (a)-[:NEAR_FOOD {distance: '1.5km', note: '当地脍炙人口小吃'}]->(f)
        """)
         session.run("""
            MATCH (a:Attraction {name: '界首博物馆'}), (f:Food {name: '板鸡'})
            CREATE (a)-[:NEAR_FOOD {distance: '0.8km', note: '特色卤味小吃'}]->(f)
        """)

        # 7. 创建关系：景点→附近住宿
         session.run("""
            MATCH (a:Attraction {name: '曹田沟景观带'}), (ac:Accommodation {name: '界首法姬娜大酒店'})
            CREATE (a)-[:NEAR_ACCOMMODATION {distance: '2km'}]->(ac)
        """)
         session.run("""
            MATCH (a:Attraction {name: '界首博物馆'}), (ac:Accommodation {name: '界首温德姆酒店'})
            CREATE (a)-[:NEAR_ACCOMMODATION {distance: '1km'}]->(ac)
        """)

        # 8. 创建关系：城市→交通及代管关系
         session.run("""
            MATCH (c:City {name: '界首'}), (t:Transportation)
            WHERE t.name IN ['界首南站', '界首公交']
            CREATE (c)-[:HAS_TRANSPORTATION]->(t)
        """)
        # 与阜阳的代管及交通关联
         session.run("""
            MATCH (c1:City {name: '界首'}), (c2:City {name: '阜阳'})
            CREATE (c1)-[:ADMINISTERED_BY {type: '代管'}]->(c2),
                   (c1)-[:CONNECTED_BY {transport: '郑阜高铁', duration: '约25分钟'}]->(c2)
        """)

        # 9. 补充博物馆文化特色提示
         session.run("""
            MATCH (a:Attraction {name: '界首博物馆'})
            SET a.cultural_feature = '可了解国家级非物质文化遗产——界首彩陶的历史与工艺'
        """)

        # 10. 补充高铁站出行提示
         session.run("""
            MATCH (t:Transportation {name: '界首南站'})
            SET t.tip = '可快速抵达阜阳、郑州、合肥等城市'
        """)

        print("界首旅游数据导入完成！")

    def import_ningguo_data(self):
        """导入宁国市旅游数据"""
        with self.driver.session() as session:
        # 1. 创建城市节点（标注县级市及代管关系）
         session.run("""
            CREATE 
            (ng:City {
                name: '宁国', 
                level: '县级市（由宣城市代管）', 
                description: '长三角绿色花园，中国山核桃之乡，元竹之乡'
            })
        """)

        # 2. 创建景点节点
         session.run("""
            CREATE 
            (qinglongwan:Attraction {
                name: '青龙湾原生态旅游区', 
                type: '自然景观', 
                rating: 4.6, 
                opening_hours: '8:30 - 17:00'
            }),
            (enlongmucun:Attraction {
                name: '恩龙世界木屋村', 
                type: '自然+人文景观', 
                rating: 4.4, 
                opening_hours: '8:00 - 17:30'
            })
        """)

        # 3. 创建美食、住宿、交通节点
         session.run("""
            CREATE 
            (ningguoshanhetao:Food {
                name: '宁国山核桃', 
                type: '地方特产', 
                price_range: '中', 
                description: '壳薄肉厚，香脆可口',
                honor: '国家地理标志产品'
            }),
            (yipingguo:Food {
                name: '一品锅', 
                type: '地方菜', 
                price_range: '中高', 
                description: '用料丰富，层层堆叠，鲜香醇厚'
            }),

            (ningguoguoji:Accommodation {
                name: '宁国国际大酒店', 
                type: '高档型酒店', 
                price_range: '中', 
                rating: 4.4
            }),
            (qinglongwanminsu:Accommodation {
                name: '青龙湾度假区民宿', 
                type: '特色民宿', 
                price_range: '中低-中高', 
                rating: 4.5
            }),

            (ningguobeizhan:Transportation {
                name: '宁国北站', 
                type: '高铁站', 
                route: '商合杭高铁沿线', 
                price: '按里程计费'
            }),
            (ningguogj:Transportation {
                name: '宁国公交', 
                type: '公交', 
                route: '覆盖主城区及部分乡镇', 
                price: '1-3元'
            })
        """)

        # 4. 创建关系：景点→城市
         session.run("""
            MATCH (a:Attraction), (c:City {name: '宁国'})
            WHERE a.name IN ['青龙湾原生态旅游区', '恩龙世界木屋村']
            CREATE (a)-[:LOCATED_IN]->(c)
        """)

        # 5. 创建关系：城市→推荐美食
         session.run("""
            MATCH (c:City {name: '宁国'}), (f:Food)
            WHERE f.name IN ['宁国山核桃', '一品锅']
            CREATE (c)-[:RECOMMENDS_FOOD]->(f)
        """)

        # 6. 创建关系：景点→附近美食（突出特产与生态关联）
         session.run("""
            MATCH (a:Attraction {name: '青龙湾原生态旅游区'}), (f:Food {name: '宁国山核桃'})
            CREATE (a)-[:NEAR_FOOD {distance: '5km', note: '必尝及馈赠佳品'}]->(f)
        """)
         session.run("""
            MATCH (a:Attraction {name: '恩龙世界木屋村'}), (f:Food {name: '一品锅'})
            CREATE (a)-[:NEAR_FOOD {distance: '3km', note: '徽菜代表作，与绩溪胡适一品锅同源'}]->(f)
        """)

        # 7. 创建关系：景点→附近住宿
         session.run("""
            MATCH (a:Attraction {name: '青龙湾原生态旅游区'}), (ac:Accommodation {name: '青龙湾度假区民宿'})
            CREATE (a)-[:NEAR_ACCOMMODATION {distance: '2km', note: '湖景民宿，推荐体验'}]->(ac)
        """)
         session.run("""
            MATCH (a:Attraction {name: '恩龙世界木屋村'}), (ac:Accommodation {name: '宁国国际大酒店'})
            CREATE (a)-[:NEAR_ACCOMMODATION {distance: '8km'}]->(ac)
        """)

        # 8. 创建关系：城市→交通及代管关系
         session.run("""
            MATCH (c:City {name: '宁国'}), (t:Transportation)
            WHERE t.name IN ['宁国北站', '宁国公交']
            CREATE (c)-[:HAS_TRANSPORTATION]->(t)
        """)
        # 与宣城的代管及交通关联
         session.run("""
            MATCH (c1:City {name: '宁国'}), (c2:City {name: '宣城'})
            CREATE (c1)-[:ADMINISTERED_BY {type: '代管'}]->(c2),
                   (c1)-[:CONNECTED_BY {transport: '商合杭高铁', duration: '约35分钟'}]->(c2)
        """)

        # 9. 补充山核桃特产提示
         session.run("""
            MATCH (f:Food {name: '宁国山核桃'})
            SET f.tip = '国家地理标志产品，推荐作为伴手礼'
        """)

        # 10. 补充青龙湾游览提示
         session.run("""
            MATCH (a:Attraction {name: '青龙湾原生态旅游区'})
            SET a.experience_tip = '可选择湖景民宿，深度体验山水之美'
        """)

        print("宁国旅游数据导入完成！")

    def import_guangde_data(self):
        """导入广德市旅游数据"""
        with self.driver.session() as session:
        # 1. 创建城市节点（标注县级市及代管关系）
         session.run("""
            CREATE 
            (gd:City {
                name: '广德', 
                level: '县级市（由宣城市代管）', 
                description: '长三角几何中心，竹海之乡，生态胜地'
            })
        """)

        # 2. 创建景点节点（突出核心景区美誉）
         session.run("""
            CREATE 
            (taijidong:Attraction {
                name: '太极洞', 
                type: '自然景观', 
                rating: 4.5, 
                opening_hours: '8:00 - 16:30',
                honor: '东南第一洞'
            }),
            (jishanzuhai:Attraction {
                name: '笄山竹海', 
                type: '自然景观', 
                rating: 4.4, 
                opening_hours: '全天开放'
            })
        """)

        # 3. 创建美食、住宿、交通节点
         session.run("""
            CREATE 
            (guangdejishansun:Food {
                name: '广德笄山笋', 
                type: '地方特产', 
                price_range: '中低', 
                description: '肉质肥厚，鲜嫩爽口'
            }),
            (qingzhentonghuayu:Food {
                name: '清蒸桐花鱼', 
                type: '地方菜', 
                price_range: '中', 
                description: '鱼肉细嫩，原汁原味'
            }),

            (muzidujia:Accommodation {
                name: '广德木子度假村', 
                type: '度假酒店', 
                price_range: '中', 
                rating: 4.4
            }),
            (hengshanbinguan:Accommodation {
                name: '广德横山宾馆', 
                type: '商务型酒店', 
                price_range: '中', 
                rating: 4.2
            }),

            (guangdenanzhan:Transportation {
                name: '广德南站', 
                type: '高铁站', 
                route: '商合杭高铁沿线', 
                price: '按里程计费'
            }),
            (guangdegj:Transportation {
                name: '广德公交', 
                type: '公交', 
                route: '覆盖主城区及主要乡镇', 
                price: '1-3元'
            })
        """)

        # 4. 创建关系：景点→城市
         session.run("""
            MATCH (a:Attraction), (c:City {name: '广德'})
            WHERE a.name IN ['太极洞', '笄山竹海']
            CREATE (a)-[:LOCATED_IN]->(c)
        """)

        # 5. 创建关系：城市→推荐美食
         session.run("""
            MATCH (c:City {name: '广德'}), (f:Food)
            WHERE f.name IN ['广德笄山笋', '清蒸桐花鱼']
            CREATE (c)-[:RECOMMENDS_FOOD]->(f)
        """)

        # 6. 创建关系：景点→附近美食（突出竹海特产关联）
         session.run("""
            MATCH (a:Attraction {name: '笄山竹海'}), (f:Food {name: '广德笄山笋'})
            CREATE (a)-[:NEAR_FOOD {distance: '2km', note: '竹海核心特产，代表性美食'}]->(f)
        """)
         session.run("""
            MATCH (a:Attraction {name: '太极洞'}), (f:Food {name: '清蒸桐花鱼'})
            CREATE (a)-[:NEAR_FOOD {distance: '6km', note: '原生态湖鲜菜品'}]->(f)
        """)

        # 7. 创建关系：景点→附近住宿
         session.run("""
            MATCH (a:Attraction {name: '笄山竹海'}), (ac:Accommodation {name: '广德木子度假村'})
            CREATE (a)-[:NEAR_ACCOMMODATION {distance: '4km', note: '度假酒店，近竹海景区'}]->(ac)
        """)
         session.run("""
            MATCH (a:Attraction {name: '太极洞'}), (ac:Accommodation {name: '广德横山宾馆'})
            CREATE (a)-[:NEAR_ACCOMMODATION {distance: '10km'}]->(ac)
        """)

        # 8. 创建关系：城市→交通及代管关系
         session.run("""
            MATCH (c:City {name: '广德'}), (t:Transportation)
            WHERE t.name IN ['广德南站', '广德公交']
            CREATE (c)-[:HAS_TRANSPORTATION]->(t)
        """)
        # 与宣城的代管及交通关联
         session.run("""
            MATCH (c1:City {name: '广德'}), (c2:City {name: '宣城'})
            CREATE (c1)-[:ADMINISTERED_BY {type: '代管'}]->(c2),
                   (c1)-[:CONNECTED_BY {transport: '商合杭高铁', duration: '约40分钟'}]->(c2)
        """)

        # 9. 补充太极洞景观特色提示
         session.run("""
            MATCH (a:Attraction {name: '太极洞'})
            SET a.landscape_feature = '喀斯特溶洞地貌，"洞天竹海"旅游品牌核心景点'
        """)

        # 10. 补充高铁站出行提示
         session.run("""
            MATCH (t:Transportation {name: '广德南站'})
            SET t.tip = '可便捷抵达杭州、合肥等城市，长三角交通便利'
        """)

        print("广德旅游数据导入完成！")

    def import_fuzhou_data(self):
        """导入福州市旅游数据"""
        with self.driver.session() as session:
         # 1. 创建城市节点（明确省会属性及城市等级）
         session.run("""
            CREATE 
            (fz:City {
                name: '福州', 
                level: '二线城市', 
                description: '福建省会，榕城，有福之州',
                province: '福建省'  // 新增省份属性，区分安徽城市
            })
        """)

        # 2. 创建景点节点（突出5A/4A景区等级）
         session.run("""
            CREATE 
            (sanfangqixiang:Attraction {
                name: '三坊七巷', 
                type: '人文景观', 
                rating: 4.7, 
                opening_hours: '全天开放 (部分小景点8:30-17:00)',
                level: '5A景区'
            }),
            (gushan:Attraction {
                name: '鼓山', 
                type: '自然+人文景观', 
                rating: 4.6, 
                opening_hours: '全天开放 (缆车及涌泉寺有时间限制)',
                level: '4A景区'
            })
        """)

        # 3. 创建美食、住宿、交通节点（突出闽菜特色）
         session.run("""
            CREATE 
            (fotiaoqiang:Food {
                name: '佛跳墙', 
                type: '闽菜', 
                price_range: '高', 
                description: '闽菜首席，用料奢华，醇香浓郁'
            }),
            (fuzhouyuwan:Food {
                name: '福州鱼丸', 
                type: '地方小吃', 
                price_range: '低', 
                description: '皮薄馅足，口感Q弹，汤味鲜美'
            }),

            (rongqiaohuangguan:Accommodation {
                name: '福州融侨皇冠假日酒店', 
                type: '五星级酒店', 
                price_range: '中高', 
                rating: 4.6
            }),
            (juchunyuan:Accommodation {
                name: '福州聚春园大酒店', 
                type: '历史文化酒店', 
                price_range: '中', 
                rating: 4.5
            }),

            (fuzhoumetro1:Transportation {
                name: '福州地铁1号线', 
                type: '地铁', 
                route: '象峰-三江口', 
                price: '2-7元'
            }),
            (konggangkuaixian:Transportation {
                name: '福州长乐国际机场空港快线', 
                type: '大巴', 
                route: '机场-市区', 
                price: '20-30元'
            })
        """)

        # 4. 创建关系：景点→城市
         session.run("""
            MATCH (a:Attraction), (c:City {name: '福州'})
            WHERE a.name IN ['三坊七巷', '鼓山']
            CREATE (a)-[:LOCATED_IN]->(c)
        """)

        # 5. 创建关系：城市→推荐美食
         session.run("""
            MATCH (c:City {name: '福州'}), (f:Food)
            WHERE f.name IN ['佛跳墙', '福州鱼丸']
            CREATE (c)-[:RECOMMENDS_FOOD]->(f)
        """)

        # 6. 创建关系：景点→附近美食（突出闽菜与小吃关联）
         session.run("""
            MATCH (a:Attraction {name: '三坊七巷'}), (f:Food {name: '福州鱼丸'})
            CREATE (a)-[:NEAR_FOOD {distance: '0.5km', note: '街头特色小吃，随处可尝'}]->(f)
        """)
         session.run("""
            MATCH (a:Attraction {name: '鼓山'}), (f:Food {name: '佛跳墙'})
            CREATE (a)-[:NEAR_FOOD {distance: '8km', note: '闽菜瑰宝，建议专程体验'}]->(f)
        """)

        # 7. 创建关系：景点→附近住宿（关联历史文化酒店特色）
         session.run("""
            MATCH (a:Attraction {name: '三坊七巷'}), (ac:Accommodation {name: '福州聚春园大酒店'})
            CREATE (a)-[:NEAR_ACCOMMODATION {distance: '1km', note: '佛跳墙发源地，体验正宗风味'}]->(ac)
        """)
         session.run("""
            MATCH (a:Attraction {name: '鼓山'}), (ac:Accommodation {name: '福州融侨皇冠假日酒店'})
            CREATE (a)-[:NEAR_ACCOMMODATION {distance: '10km'}]->(ac)
        """)

        # 8. 创建关系：城市→交通及换乘关联
         session.run("""
            MATCH (c:City {name: '福州'}), (t:Transportation)
            WHERE t.name IN ['福州地铁1号线', '福州长乐国际机场空港快线']
            CREATE (c)-[:HAS_TRANSPORTATION]->(t)
        """)
        # 地铁与空港快线换乘关系
         session.run("""
            MATCH (t1:Transportation {name: '福州地铁1号线'}), (t2:Transportation {name: '福州长乐国际机场空港快线'})
            CREATE (t1)-[:CONNECTED_TO {description: '便捷换乘，快速抵达机场'}]->(t2)
        """)

        # 9. 补充聚春园酒店特色提示
         session.run("""
            MATCH (ac:Accommodation {name: '福州聚春园大酒店'})
            SET ac.features = '佛跳墙发源地，兼具历史文化与美食体验'
        """)

        # 10. 补充三坊七巷游览提示
         session.run("""
            MATCH (a:Attraction {name: '三坊七巷'})
            SET a.tip = '核心历史文化街区，建议预留2-3小时深度游览'
        """)

        print("福州旅游数据导入完成！")

    def import_xiamen_data(self):
        """导入厦门市旅游数据"""
        with self.driver.session() as session:
        # 1. 创建城市节点（明确经济特区属性）
         session.run("""
            CREATE 
            (xm:City {
                name: '厦门', 
                level: '二线城市', 
                description: '经济特区，海上花园，高素质高颜值现代化国际化城市',
                province: '福建省',
                feature: '经济特区'  // 突出特区属性
            })
        """)

        # 2. 创建景点节点（强化世界文化遗产标签）
         session.run("""
            CREATE 
            (gulangyu:Attraction {
                name: '鼓浪屿', 
                type: '自然+人文景观', 
                rating: 4.8, 
                opening_hours: '全天开放 (部分景点有时间限制)',
                honor: '世界文化遗产'
            }),
            (yuanlinzhiwuyuan:Attraction {
                name: '厦门园林植物园', 
                type: '自然景观', 
                rating: 4.7, 
                opening_hours: '6:30 - 18:00'
            })
        """)

        # 3. 创建美食、住宿、交通节点（突出海滨城市特色）
         session.run("""
            CREATE 
            (shachamian:Food {
                name: '沙茶面', 
                type: '地方小吃', 
                price_range: '中低', 
                description: '汤头浓郁，配料自选，风味独特'
            }),
            (jiangmuya:Food {
                name: '姜母鸭', 
                type: '地方菜', 
                price_range: '中', 
                description: '食色诱人，香气扑鼻，温而不燥'
            }),

            (qishangjiudian:Accommodation {
                name: '厦门七尚酒店', 
                type: '奢华型酒店', 
                price_range: '高', 
                rating: 4.8
            }),
            (kanglaidejiudian:Accommodation {
                name: '厦门康莱德酒店', 
                type: '五星级酒店', 
                price_range: '高', 
                rating: 4.7
            }),

            (xiamenditie1:Transportation {
                name: '厦门地铁1号线', 
                type: '地铁', 
                route: '镇海路站-岩内站', 
                price: '2-7元'
            }),
            (xiagulundu:Transportation {
                name: '厦鼓轮渡', 
                type: '轮渡', 
                route: '厦门岛-鼓浪屿', 
                price: '35元起 (游客航线)'
            })
        """)

        # 4. 创建关系：景点→城市
         session.run("""
            MATCH (a:Attraction), (c:City {name: '厦门'})
            WHERE a.name IN ['鼓浪屿', '厦门园林植物园']
            CREATE (a)-[:LOCATED_IN]->(c)
        """)

        # 5. 创建关系：城市→推荐美食
         session.run("""
            MATCH (c:City {name: '厦门'}), (f:Food)
            WHERE f.name IN ['沙茶面', '姜母鸭']
            CREATE (c)-[:RECOMMENDS_FOOD]->(f)
        """)

        # 6. 创建关系：景点→附近美食（结合海滨游览场景）
         session.run("""
            MATCH (a:Attraction {name: '鼓浪屿'}), (f:Food {name: '沙茶面'})
            CREATE (a)-[:NEAR_FOOD {distance: '0.3km', note: '岛上特色小吃店遍布'}]->(f)
        """)
         session.run("""
            MATCH (a:Attraction {name: '厦门园林植物园'}), (f:Food {name: '姜母鸭'})
            CREATE (a)-[:NEAR_FOOD {distance: '2km', note: '周边老字号餐馆推荐'}]->(f)
        """)

        # 7. 创建关系：景点→附近住宿（突出海景特色）
         session.run("""
            MATCH (a:Attraction {name: '鼓浪屿'}), (ac:Accommodation {name: '厦门康莱德酒店'})
            CREATE (a)-[:NEAR_ACCOMMODATION {distance: '1.5km', note: '可俯瞰鼓浪屿海景'}]->(ac)
        """)
         session.run("""
            MATCH (a:Attraction {name: '厦门园林植物园'}), (ac:Accommodation {name: '厦门七尚酒店'})
            CREATE (a)-[:NEAR_ACCOMMODATION {distance: '5km'}]->(ac)
        """)

        # 8. 创建关系：城市→交通及关键关联
         session.run("""
            MATCH (c:City {name: '厦门'}), (t:Transportation)
            WHERE t.name IN ['厦门地铁1号线', '厦鼓轮渡']
            CREATE (c)-[:HAS_TRANSPORTATION]->(t)
        """)
        # 地铁与轮渡换乘关系
         session.run("""
            MATCH (t1:Transportation {name: '厦门地铁1号线'}), (t2:Transportation {name: '厦鼓轮渡'})
            CREATE (t1)-[:CONNECTED_TO {transfer_station: '镇海路站', walking_time: '10分钟'}]->(t2)
        """)

        # 9. 补充鼓浪屿游览提示
         session.run("""
            MATCH (a:Attraction {name: '鼓浪屿'})
            SET a.tip = '需提前通过官方渠道预订厦鼓轮渡船票，建议安排1天深度游览'
        """)

        # 10. 补充康莱德酒店特色
         session.run("""
            MATCH (ac:Accommodation {name: '厦门康莱德酒店'})
            SET ac.view_feature = '位于世茂海峡大厦，可俯瞰鼓浪屿及厦港片区海景'
        """)

        print("厦门旅游数据导入完成！")

    def import_quanzhou_data(self):
        """导入泉州市旅游数据"""
        with self.driver.session() as session:
        # 1. 创建城市节点（突出文化与历史地位）
         session.run("""
            CREATE 
            (qz:City {
                name: '泉州', 
                level: '二线城市', 
                description: '东亚文化之都，海上丝绸之路起点，世界宗教博物馆',
                province: '福建省',
                honor: '联合国三大类非遗项目拥有城市'  // 突出非遗特色
            })
        """)

        # 2. 创建景点节点（强化5A景区及文化地标属性）
         session.run("""
            CREATE 
            (qingyuanshan:Attraction {
                name: '清源山', 
                type: '自然+人文景观', 
                rating: 4.7, 
                opening_hours: '7:00 - 23:59（早7点前&晚6点后免费）',
                level: '5A景区',
                feature: '拥有老君岩石刻等标志性文化遗迹'
            }),
            (kaiyuansi:Attraction {
                name: '开元寺', 
                type: '人文景观', 
                rating: 4.9, 
                opening_hours: '6:30 - 17:30',
                feature: '东西双塔为泉州城市标志'
            })
        """)

        # 3. 创建美食、住宿、交通节点（突出地方饮食文化）
         session.run("""
            CREATE 
            (mianxianhu:Food {
                name: '面线糊', 
                type: '地方小吃', 
                price_range: '低', 
                description: '口感细腻顺滑，可搭配醋肉、大肠等配料，是泉州经典早餐'
            }),
            (quanzhourouzong:Food {
                name: '泉州肉粽', 
                type: '地方主食', 
                price_range: '中低', 
                description: '用料扎实，包裹猪肉、干贝等食材，糯米软糯，香气浓郁'
            }),

            (yuehuajiudian:Accommodation {
                name: '泉州悦华酒店', 
                type: '五星级酒店', 
                price_range: '中高', 
                rating: 4.6,
                nearby_attraction: '领SHOW天地创艺乐园'
            }),
            (yingbinguan:Accommodation {
                name: '泉州迎宾馆', 
                type: '五星级酒店', 
                price_range: '中高', 
                rating: 4.5,
                nearby_attraction: '泉州森林公园'
            }),

            (gongjiaoK1:Transportation {
                name: '泉州公交K1路', 
                type: '公交', 
                route: '福厦铁路泉州站-文化宫', 
                price: '1-2元（常规票价）'
            }),
            (quanzhoudongzhan:Transportation {
                name: '福厦高铁泉州站', 
                type: '高铁站', 
                route: '连接福州、厦门等城市', 
                price: '按具体里程定价'
            })
        """)

        # 4. 创建关系：景点→城市
         session.run("""
            MATCH (a:Attraction), (c:City {name: '泉州'})
            WHERE a.name IN ['清源山', '开元寺']
            CREATE (a)-[:LOCATED_IN]->(c)
        """)

        # 5. 创建关系：城市→推荐美食
         session.run("""
            MATCH (c:City {name: '泉州'}), (f:Food)
            WHERE f.name IN ['面线糊', '泉州肉粽']
            CREATE (c)-[:RECOMMENDS_FOOD]->(f)
        """)

        # 6. 创建关系：景点→附近美食（结合日常饮食场景）
         session.run("""
            MATCH (a:Attraction {name: '开元寺'}), (f:Food {name: '面线糊'})
            CREATE (a)-[:NEAR_FOOD {distance: '0.8km', note: '周边老字号早餐店推荐，搭配油条更佳'}]->(f)
        """)
         session.run("""
            MATCH (a:Attraction {name: '清源山'}), (f:Food {name: '泉州肉粽'})
            CREATE (a)-[:NEAR_FOOD {distance: '3km', note: '景区出口处可品尝热乎肉粽'}]->(f)
        """)

        # 7. 创建关系：景点→附近住宿（关联周边特色）
         session.run("""
            MATCH (a:Attraction {name: '开元寺'}), (ac:Accommodation {name: '泉州悦华酒店'})
            CREATE (a)-[:NEAR_ACCOMMODATION {distance: '2km', note: '近创艺园区，适合年轻游客'}]->(ac)
        """)
         session.run("""
            MATCH (a:Attraction {name: '清源山'}), (ac:Accommodation {name: '泉州迎宾馆'})
            CREATE (a)-[:NEAR_ACCOMMODATION {distance: '4km', note: '毗邻森林公园，环境清幽'}]->(ac)
        """)

        # 8. 创建关系：城市→交通及换乘关联
         session.run("""
            MATCH (c:City {name: '泉州'}), (t:Transportation)
            WHERE t.name IN ['泉州公交K1路', '福厦高铁泉州站']
            CREATE (c)-[:HAS_TRANSPORTATION]->(t)
        """)
        # 高铁与公交接驳关系
         session.run("""
            MATCH (t1:Transportation {name: '福厦高铁泉州站'}), (t2:Transportation {name: '泉州公交K1路'})
            CREATE (t1)-[:CONNECTED_TO {description: '高铁出站可直接换乘，直达市中心'}]->(t2)
        """)

        # 9. 补充非遗文化体验提示
         session.run("""
            MATCH (c:City {name: '泉州'})
            SET c.cultural_tip = '可顺路体验南音、木偶戏等联合国非遗项目'
        """)

        # 10. 补充清源山游览提示
         session.run("""
            MATCH (a:Attraction {name: '清源山'})
            SET a.visit_tip = '早7点前或晚6点后入园免费，适合安排晨练或夜游'
        """)

        print("泉州旅游数据导入完成！")

    def import_putian_data(self):
        """导入莆田市旅游数据"""
        with self.driver.session() as session:
        # 1. 创建城市节点（突出文化与产业特色）
         session.run("""
            CREATE 
            (pt:City {
                name: '莆田', 
                level: '三线城市', 
                description: '妈祖故里，莆商之乡，海滨邹鲁',
                province: '福建省',
                industry_feature: '民营医疗、木材、珠宝等行业莆商发源地'
            })
        """)

        # 2. 创建景点节点（强化4A景区及文化地标属性）
         session.run("""
            CREATE 
            (meizhoudaomazu:Attraction {
                name: '湄洲岛妈祖祖庙', 
                type: '人文景观', 
                rating: 4.7, 
                opening_hours: '全天开放 (祖庙建筑群7:00-19:00)',
                level: '4A景区',
                cultural_significance: '全球妈祖文化信仰核心地'
            }),
            (nanshaolin:Attraction {
                name: '南少林寺', 
                type: '人文景观', 
                rating: 4.3, 
                opening_hours: '8:00 - 17:00',
                cultural_significance: '南少林武术文化发源地之一'
            })
        """)

        # 3. 创建美食、住宿、交通节点（突出地方饮食特色）
         session.run("""
            CREATE 
            (putianlumian:Food {
                name: '莆田卤面', 
                type: '地方主食', 
                price_range: '中低', 
                description: '用料丰富，汤汁浓稠，味道鲜美',
                scene: '宴席主菜'
            }),
            (xinghuachaomifen:Food {
                name: '兴化炒米粉', 
                type: '地方小吃', 
                price_range: '低', 
                description: '细如发丝，口感柔韧，干香入味',
                scene: '家常风味'
            }),

            (sandixilundun:Accommodation {
                name: '莆田三迪希尔顿逸林酒店', 
                type: '五星级酒店', 
                price_range: '中高', 
                rating: 4.5
            }),
            (meizhoudaojunya:Accommodation {
                name: '湄洲岛国际会展中心郡雅酒店', 
                type: '豪华型酒店', 
                price_range: '中', 
                rating: 4.4,
                location_feature: '近湄洲岛景区，方便朝拜与游览'
            }),

            (putianzhan:Transportation {
                name: '莆田站', 
                type: '高铁站', 
                route: '福厦高铁沿线', 
                price: '按里程计费'
            }),
            (pumeichengji:Transportation {
                name: '莆湄城际公交', 
                type: '公交', 
                route: '莆田市区-文甲码头(往湄洲岛)', 
                price: '10-15元'
            })
        """)

        # 4. 创建关系：景点→城市
         session.run("""
            MATCH (a:Attraction), (c:City {name: '莆田'})
            WHERE a.name IN ['湄洲岛妈祖祖庙', '南少林寺']
            CREATE (a)-[:LOCATED_IN]->(c)
        """)

        # 5. 创建关系：城市→推荐美食
         session.run("""
            MATCH (c:City {name: '莆田'}), (f:Food)
            WHERE f.name IN ['莆田卤面', '兴化炒米粉']
            CREATE (c)-[:RECOMMENDS_FOOD]->(f)
        """)

        # 6. 创建关系：景点→附近美食（结合场景化饮食需求）
         session.run("""
            MATCH (a:Attraction {name: '南少林寺'}), (f:Food {name: '莆田卤面'})
            CREATE (a)-[:NEAR_FOOD {distance: '5km', note: '景区周边餐馆可尝宴席级卤面'}]->(f)
        """)
         session.run("""
            MATCH (a:Attraction {name: '湄洲岛妈祖祖庙'}), (f:Food {name: '兴化炒米粉'})
            CREATE (a)-[:NEAR_FOOD {distance: '1km', note: '岛上小吃店可品家常炒米粉'}]->(f)
        """)

        # 7. 创建关系：景点→附近住宿（匹配景区位置）
         session.run("""
            MATCH (a:Attraction {name: '南少林寺'}), (ac:Accommodation {name: '莆田三迪希尔顿逸林酒店'})
            CREATE (a)-[:NEAR_ACCOMMODATION {distance: '12km', note: '市区高端酒店，适合商务+旅游'}]->(ac)
        """)
         session.run("""
            MATCH (a:Attraction {name: '湄洲岛妈祖祖庙'}), (ac:Accommodation {name: '湄洲岛国际会展中心郡雅酒店'})
            CREATE (a)-[:NEAR_ACCOMMODATION {distance: '2km', note: '岛上豪华酒店，方便朝拜后休整'}]->(ac)
        """)

        # 8. 创建关系：城市→交通及关键接驳
         session.run("""
            MATCH (c:City {name: '莆田'}), (t:Transportation)
            WHERE t.name IN ['莆田站', '莆湄城际公交']
            CREATE (c)-[:HAS_TRANSPORTATION]->(t)
        """)
        # 高铁与城际公交换乘提示
         session.run("""
            MATCH (t1:Transportation {name: '莆田站'}), (t2:Transportation {name: '莆湄城际公交'})
            CREATE (t1)-[:CONNECTED_TO {description: '出站可换乘，直达文甲码头'}]->(t2)
        """)

        # 9. 补充湄洲岛游览关键提示
         session.run("""
            MATCH (a:Attraction {name: '湄洲岛妈祖祖庙'})
            SET a.visit_tip = '前往湄洲岛需在文甲码头乘坐轮渡，建议提前查询航班时间'
        """)

        # 10. 补充莆商文化提示
         session.run("""
            MATCH (c:City {name: '莆田'})
            SET c.business_culture = '莆商文化底蕴深厚，民营医疗、木材、珠宝等产业闻名全国'
        """)

        print("莆田旅游数据导入完成！")

    def import_sanming_data(self):
        """导入三明市旅游数据"""
        with self.driver.session() as session:
        # 1. 创建城市节点（突出生态与文化定位）
         session.run("""
            CREATE 
            (sm:City {
                name: '三明', 
                level: '四线城市', 
                description: '中国绿都，沙溪河畔文明城，朱子理学发扬地',
                province: '福建省',
                ecological_feature: '森林覆盖率极高，生态旅游胜地'
            })
        """)

        # 2. 创建景点节点（强化世界地质公园属性）
         session.run("""
            CREATE 
            (tainingfengjing:Attraction {
                name: '泰宁风景旅游区', 
                type: '自然+人文景观', 
                rating: 4.7, 
                opening_hours: '8:00 - 17:00 (各子景区不同)',
                honor: '世界地质公园',
                sub_attraction: '含大金湖、上清溪等子景区'
            }),
            (taoyuandong:Attraction {
                name: '桃源洞', 
                type: '自然景观', 
                rating: 4.4, 
                opening_hours: '8:00 - 17:00'
            })
        """)

        # 3. 创建美食、住宿、交通节点（突出小吃文化特色）
         session.run("""
            CREATE 
            (shaxianxiaochi:Food {
                name: '沙县小吃（拌面、扁肉）', 
                type: '地方小吃', 
                price_range: '低', 
                description: '闻名全国，经济实惠，风味独特',
                honor: '地方特色名片，发源地正宗风味'
            }),
            (yonganguotiao:Food {
                name: '永安粿条', 
                type: '地方小吃', 
                price_range: '低', 
                description: '口感爽滑，汤头鲜醇'
            }),

            (tianyuanguoji:Accommodation {
                name: '三明天元国际大酒店', 
                type: '高档型酒店', 
                price_range: '中', 
                rating: 4.3
            }),
            (tainingchenshi:Accommodation {
                name: '泰宁晟世酒店', 
                type: '度假酒店', 
                price_range: '中', 
                rating: 4.5,
                location_feature: '近泰宁风景旅游区，方便生态游览'
            }),

            (sanmingzhan:Transportation {
                name: '三明站', 
                type: '高铁站', 
                route: '南龙铁路沿线', 
                price: '按里程计费'
            }),
            (sanminggongjiao:Transportation {
                name: '三明公交', 
                type: '公交', 
                route: '覆盖市区', 
                price: '1-2元'
            })
        """)

        # 4. 创建关系：景点→城市
         session.run("""
            MATCH (a:Attraction), (c:City {name: '三明'})
            WHERE a.name IN ['泰宁风景旅游区', '桃源洞']
            CREATE (a)-[:LOCATED_IN]->(c)
        """)

        # 5. 创建关系：城市→推荐美食
         session.run("""
            MATCH (c:City {name: '三明'}), (f:Food)
            WHERE f.name IN ['沙县小吃（拌面、扁肉）', '永安粿条']
            CREATE (c)-[:RECOMMENDS_FOOD]->(f)
        """)

        # 6. 创建关系：景点→附近美食（结合小吃文化场景）
         session.run("""
            MATCH (a:Attraction {name: '桃源洞'}), (f:Food {name: '沙县小吃（拌面、扁肉）'})
            CREATE (a)-[:NEAR_FOOD {distance: '15km', note: '景区周边可尝发源地正宗小吃'}]->(f)
        """)
         session.run("""
            MATCH (a:Attraction {name: '泰宁风景旅游区'}), (f:Food {name: '永安粿条'})
            CREATE (a)-[:NEAR_FOOD {distance: '8km', note: '当地特色小吃，搭配游览体验'}]->(f)
        """)

        # 7. 创建关系：景点→附近住宿（匹配生态旅游需求）
         session.run("""
            MATCH (a:Attraction {name: '桃源洞'}), (ac:Accommodation {name: '三明天元国际大酒店'})
            CREATE (a)-[:NEAR_ACCOMMODATION {distance: '20km', note: '市区高档酒店，适合商务+旅游'}]->(ac)
        """)
         session.run("""
            MATCH (a:Attraction {name: '泰宁风景旅游区'}), (ac:Accommodation {name: '泰宁晟世酒店'})
            CREATE (a)-[:NEAR_ACCOMMODATION {distance: '3km', note: '近景区，方便深度体验生态风光'}]->(ac)
        """)

        # 8. 创建关系：城市→交通及关联
         session.run("""
            MATCH (c:City {name: '三明'}), (t:Transportation)
            WHERE t.name IN ['三明站', '三明公交']
            CREATE (c)-[:HAS_TRANSPORTATION]->(t)
        """)

        # 9. 补充泰宁古城文化提示
         session.run("""
            MATCH (a:Attraction {name: '泰宁风景旅游区'})
            SET a.cultural_tip = '含泰宁古城，保存完好明代建筑群，蕴含深厚科举文化'
        """)

        # 10. 补充生态旅游提示
         session.run("""
            MATCH (c:City {name: '三明'})
            SET c.ecological_tip = '森林覆盖率高，"中国绿都"，适合生态旅游与深呼吸体验'
        """)

        print("三明旅游数据导入完成！")

    def import_zhangzhou_data(self):
        """导入漳州市旅游数据"""
        with self.driver.session() as session:
        # 1. 创建城市节点（突出闽南文化与生态定位）
         session.run("""
            CREATE 
            (zz:City {
                name: '漳州', 
                level: '三线城市', 
                description: '田园都市，生态之城，水仙花之乡，闽南文化发祥地之一',
                province: '福建省',
                cultural_connection: '台湾同胞重要祖籍地之一，闽南文化底蕴深厚'
            })
        """)

        # 2. 创建景点节点（强化世界遗产与滨海属性）
         session.run("""
            CREATE 
            (nanjingtulou:Attraction {
                name: '南靖土楼（田螺坑、云水谣）', 
                type: '人文景观', 
                rating: 4.7, 
                opening_hours: '全天开放 (部分楼馆8:00-17:30)',
                honor: '世界遗产',
                feature: '客家文化标志性建筑，"四菜一汤"布局闻名'
            }),
            (dongshandao:Attraction {
                name: '东山岛（风动石、马銮湾）', 
                type: '自然景观', 
                rating: 4.6, 
                opening_hours: '全天开放 (风动石景区7:30-18:00)',
                feature: '滨海风光，含风动石奇观与优质沙滩'
            })
        """)

        # 3. 创建美食、住宿、交通节点（突出闽南饮食特色）
         session.run("""
            CREATE 
            (zhangzhoulumian:Food {
                name: '漳州卤面', 
                type: '地方主食', 
                price_range: '中低', 
                description: '汤汁浓稠，配料丰富，风味独特',
                scene: '节庆必备主食'
            }),
            (haolijian:Food {
                name: '蚵仔煎（海蛎煎）', 
                type: '地方小吃', 
                price_range: '中低', 
                description: '外酥内嫩，鲜香可口'
            }),

            (wandajiahua:Accommodation {
                name: '漳州万达嘉华酒店', 
                type: '五星级酒店', 
                price_range: '中高', 
                rating: 4.5
            }),
            (dongshandaozhensu:Accommodation {
                name: '东山岛一个庐野奢帐篷营地', 
                type: '特色民宿', 
                price_range: '高', 
                rating: 4.8,
                experience: '滨海野奢体验，直面海景'
            }),

            (zhangzhoutan:Transportation {
                name: '漳州站', 
                type: '高铁站', 
                route: '厦深铁路、福厦高铁沿线', 
                price: '按里程计费'
            }),
            (zhangzhougongjiao:Transportation {
                name: '漳州公交', 
                type: '公交', 
                route: '覆盖市区及主要区县', 
                price: '1-5元'
            })
        """)

        # 4. 创建关系：景点→城市
         session.run("""
            MATCH (a:Attraction), (c:City {name: '漳州'})
            WHERE a.name IN ['南靖土楼（田螺坑、云水谣）', '东山岛（风动石、马銮湾）']
            CREATE (a)-[:LOCATED_IN]->(c)
        """)

        # 5. 创建关系：城市→推荐美食
         session.run("""
            MATCH (c:City {name: '漳州'}), (f:Food)
            WHERE f.name IN ['漳州卤面', '蚵仔煎（海蛎煎）']
            CREATE (c)-[:RECOMMENDS_FOOD]->(f)
        """)

        # 6. 创建关系：景点→附近美食（结合地域饮食场景）
         session.run("""
            MATCH (a:Attraction {name: '南靖土楼（田螺坑、云水谣）'}), (f:Food {name: '漳州卤面'})
            CREATE (a)-[:NEAR_FOOD {distance: '8km', note: '客家餐馆可尝节庆版卤面'}]->(f)
        """)
         session.run("""
            MATCH (a:Attraction {name: '东山岛（风动石、马銮湾）'}), (f:Food {name: '蚵仔煎（海蛎煎）'})
            CREATE (a)-[:NEAR_FOOD {distance: '1km', note: '海边排档现做，用新鲜海蛎'}]->(f)
        """)

        # 7. 创建关系：景点→附近住宿（匹配景观类型）
         session.run("""
            MATCH (a:Attraction {name: '南靖土楼（田螺坑、云水谣）'}), (ac:Accommodation {name: '漳州万达嘉华酒店'})
            CREATE (a)-[:NEAR_ACCOMMODATION {distance: '60km', note: '市区高端酒店，适合行程中转'}]->(ac)
        """)
         session.run("""
            MATCH (a:Attraction {name: '东山岛（风动石、马銮湾）'}), (ac:Accommodation {name: '东山岛一个庐野奢帐篷营地'})
            CREATE (a)-[:NEAR_ACCOMMODATION {distance: '2km', note: '滨海特色住宿，沉浸式体验海岛风光'}]->(ac)
        """)

        # 8. 创建关系：城市→交通及关联
         session.run("""
            MATCH (c:City {name: '漳州'}), (t:Transportation)
            WHERE t.name IN ['漳州站', '漳州公交']
            CREATE (c)-[:HAS_TRANSPORTATION]->(t)
        """)

        # 9. 补充土楼游览提示
         session.run("""
            MATCH (a:Attraction {name: '南靖土楼（田螺坑、云水谣）'})
            SET a.visit_tip = '建议入住景区内特色民宿，深度体验客家风情与土楼文化'
        """)

        # 10. 补充水仙花文化提示
         session.run("""
            MATCH (c:City {name: '漳州'})
            SET c.specialty_tip = '水仙花之乡，冬季可观赏正宗漳州水仙，为中国十大名花之一'
        """)

        print("漳州旅游数据导入完成！")

    def import_nanping_data(self):
        """导入南平市旅游数据"""
        with self.driver.session() as session:
        # 1. 创建城市节点（突出双遗产与理学文化定位）
         session.run("""
            CREATE 
            (np:City {
                name: '南平', 
                level: '四线城市', 
                description: '武夷山下朱子故里，中国竹乡，八闽屏障',
                province: '福建省',
                cultural_core: '理学宗师朱熹长期生活、讲学地，朱子文化遗存丰富'
            })
        """)

        # 2. 创建景点节点（强化世界双遗产属性）
         session.run("""
            CREATE 
            (wuyishan:Attraction {
                name: '武夷山', 
                type: '自然+人文景观', 
                rating: 4.8, 
                opening_hours: '7:30 - 17:30 (各景点略有不同)',
                honor: '世界文化与自然双遗产',
                feature: '以丹霞地貌、九曲溪及茶文化闻名'
            }),
            (xiameiguminju:Attraction {
                name: '下梅古民居', 
                type: '人文景观', 
                rating: 4.4, 
                opening_hours: '7:30 - 17:30',
                feature: '明清古村落，茶商文化遗迹丰富'
            })
        """)

        # 3. 创建美食、住宿、交通节点（突出文化与生态特色）
         session.run("""
            CREATE 
            (languxunge:Food {
                name: '岚谷熏鹅', 
                type: '地方特色', 
                price_range: '中', 
                description: '色泽金黄，烟香浓郁，肉质紧实',
                origin: '武夷山特产'
            }),
            (wengongcai:Food {
                name: '文公菜', 
                type: '地方菜', 
                price_range: '中', 
                description: '为纪念朱熹而创，用料讲究，口感丰富',
                cultural_meaning: '蕴含朱子理学饮食文化'
            }),

            (wuyishanjiaye:Accommodation {
                name: '武夷山嘉叶山舍', 
                type: '奢华度假酒店', 
                price_range: '高', 
                rating: 4.8,
                feature: '近景区，融合茶文化主题'
            }),
            (wuyishanzhuang:Accommodation {
                name: '南平武夷山庄', 
                type: '国宾馆', 
                price_range: '中高', 
                rating: 4.6,
                location: '毗邻武夷山景区入口'
            }),

            (nanpingshi:Transportation {
                name: '南平市站', 
                type: '高铁站', 
                route: '合福高铁沿线', 
                price: '按里程计费'
            }),
            (wuyishanguidao:Transportation {
                name: '武夷山有轨电车', 
                type: '旅游交通', 
                route: '高铁南平市站-武夷山景区', 
                price: '10元'
            })
        """)

        # 4. 创建关系：景点→城市
         session.run("""
            MATCH (a:Attraction), (c:City {name: '南平'})
            WHERE a.name IN ['武夷山', '下梅古民居']
            CREATE (a)-[:LOCATED_IN]->(c)
        """)

        # 5. 创建关系：城市→推荐美食
         session.run("""
            MATCH (c:City {name: '南平'}), (f:Food)
            WHERE f.name IN ['岚谷熏鹅', '文公菜']
            CREATE (c)-[:RECOMMENDS_FOOD]->(f)
        """)

        # 6. 创建关系：景点→附近美食（结合文化与地域特色）
         session.run("""
            MATCH (a:Attraction {name: '武夷山'}), (f:Food {name: '岚谷熏鹅'})
            CREATE (a)-[:NEAR_FOOD {distance: '12km', note: '景区周边农家菜馆推荐'}]->(f)
        """)
         session.run("""
            MATCH (a:Attraction {name: '下梅古民居'}), (f:Food {name: '文公菜'})
            CREATE (a)-[:NEAR_FOOD {distance: '3km', note: '古村落内可尝正宗朱子文化菜'}]->(f)
        """)

        # 7. 创建关系：景点→附近住宿（匹配景区深度体验）
         session.run("""
            MATCH (a:Attraction {name: '武夷山'}), (ac:Accommodation {name: '武夷山嘉叶山舍'})
            CREATE (a)-[:NEAR_ACCOMMODATION {distance: '5km', note: '奢华度假体验，茶主题沉浸'}]->(ac)
        """)
         session.run("""
            MATCH (a:Attraction {name: '下梅古民居'}), (ac:Accommodation {name: '南平武夷山庄'})
            CREATE (a)-[:NEAR_ACCOMMODATION {distance: '8km', note: '国宾馆品质，方便多景点游览'}]->(ac)
        """)

        # 8. 创建关系：城市→交通及旅游接驳
         session.run("""
            MATCH (c:City {name: '南平'}), (t:Transportation)
            WHERE t.name IN ['南平市站', '武夷山有轨电车']
            CREATE (c)-[:HAS_TRANSPORTATION]->(t)
        """)
        # 高铁与景区专线接驳关系
         session.run("""
            MATCH (t1:Transportation {name: '南平市站'}), (t2:Transportation {name: '武夷山有轨电车'})
            CREATE (t1)-[:CONNECTED_TO {description: '无缝换乘，直达景区', duration: '约30分钟'}]->(t2)
        """)

        # 9. 补充武夷山核心体验提示
         session.run("""
            MATCH (a:Attraction {name: '武夷山'})
            SET a.core_experience = '九曲溪竹筏漂流为核心项目，建议提前3-5天通过官方渠道预订'
        """)

        # 10. 补充朱子文化体验提示
         session.run("""
            MATCH (c:City {name: '南平'})
            SET c.cultural_experience = '可参观朱熹故里、书院遗址，参与朱子家训文化活动'
        """)

        print("南平旅游数据导入完成！")

    def import_longyan_data(self):
        """导入龙岩市旅游数据"""
        with self.driver.session() as session:
        # 1. 创建城市节点（突出客家与红色文化定位）
         session.run("""
            CREATE 
            (ly:City {
                name: '龙岩', 
                level: '四线城市', 
                description: '客家祖地，红色圣地，生态福地',
                province: '福建省',
                cultural_identity: '客家民系重要形成地和祖籍地，闽西革命老区'
            })
        """)

        # 2. 创建景点节点（强化世界遗产与红色属性）
         session.run("""
            CREATE 
            (yongdingtulou:Attraction {
                name: '永定土楼（洪坑、高北）', 
                type: '人文景观', 
                rating: 4.7, 
                opening_hours: '全天开放 (部分楼馆8:00-17:30)',
                honor: '世界遗产',
                feature: '含振成楼、承启楼等不同风格客家土楼'
            }),
            (gudianhuiyi:Attraction {
                name: '古田会议旧址', 
                type: '人文景观', 
                rating: 4.6, 
                opening_hours: '8:30 - 17:00',
                feature: '红色旅游核心景点，革命历史重要见证'
            })
        """)

        # 3. 创建美食、住宿、交通节点（突出客家饮食特色）
         session.run("""
            CREATE 
            (kejibojiban:Food {
                name: '客家簸箕板', 
                type: '地方小吃', 
                price_range: '低', 
                description: '皮滑馅香，清爽可口',
                cultural_tie: '客家传统早餐，体现客家饮食智慧'
            }),
            (baizhanhetianji:Food {
                name: '白斩河田鸡', 
                type: '地方菜', 
                price_range: '中', 
                description: '金黄油亮，皮脆肉嫩，香鲜爽口',
                honor: '客家第一大菜，中国名鸡之一'
            }),

            (baixiangjinghua:Accommodation {
                name: '龙岩佰翔京华酒店', 
                type: '五星级酒店', 
                price_range: '中高', 
                rating: 4.5
            }),
            (yongdingwangzi:Accommodation {
                name: '永定土楼王子酒店', 
                type: '特色酒店', 
                price_range: '中', 
                rating: 4.4,
                feature: '土楼风格建筑，沉浸式客家体验'
            }),

            (longyanzhan:Transportation {
                name: '龙岩站', 
                type: '高铁站', 
                route: '南龙铁路、赣瑞龙铁路', 
                price: '按里程计费'
            }),
            (longyangongjiao:Transportation {
                name: '龙岩公交', 
                type: '公交', 
                route: '覆盖市区及主要县市', 
                price: '1-5元'
            })
        """)

        # 4. 创建关系：景点→城市
         session.run("""
            MATCH (a:Attraction), (c:City {name: '龙岩'})
            WHERE a.name IN ['永定土楼（洪坑、高北）', '古田会议旧址']
            CREATE (a)-[:LOCATED_IN]->(c)
        """)

        # 5. 创建关系：城市→推荐美食
         session.run("""
            MATCH (c:City {name: '龙岩'}), (f:Food)
            WHERE f.name IN ['客家簸箕板', '白斩河田鸡']
            CREATE (c)-[:RECOMMENDS_FOOD]->(f)
        """)

        # 6. 创建关系：景点→附近美食（结合文化场景）
         session.run("""
            MATCH (a:Attraction {name: '永定土楼（洪坑、高北）'}), (f:Food {name: '客家簸箕板'})
            CREATE (a)-[:NEAR_FOOD {distance: '2km', note: '土楼周边客家餐馆随处可见'}]->(f)
        """)
         session.run("""
            MATCH (a:Attraction {name: '古田会议旧址'}), (f:Food {name: '白斩河田鸡'})
            CREATE (a)-[:NEAR_FOOD {distance: '5km', note: '当地农庄可品尝正宗河田鸡'}]->(f)
        """)

        # 7. 创建关系：景点→附近住宿（匹配文化体验）
         session.run("""
            MATCH (a:Attraction {name: '永定土楼（洪坑、高北）'}), (ac:Accommodation {name: '永定土楼王子酒店'})
            CREATE (a)-[:NEAR_ACCOMMODATION {distance: '1km', note: '土楼风格酒店，体验客家生活'}]->(ac)
        """)
         session.run("""
            MATCH (a:Attraction {name: '古田会议旧址'}), (ac:Accommodation {name: '龙岩佰翔京华酒店'})
            CREATE (a)-[:NEAR_ACCOMMODATION {distance: '30km', note: '市区高端酒店，适合红色旅游中转'}]->(ac)
        """)

        # 8. 创建关系：城市→交通及关联
         session.run("""
            MATCH (c:City {name: '龙岩'}), (t:Transportation)
            WHERE t.name IN ['龙岩站', '龙岩公交']
            CREATE (c)-[:HAS_TRANSPORTATION]->(t)
        """)

        # 9. 补充土楼游览提示
         session.run("""
            MATCH (a:Attraction {name: '永定土楼（洪坑、高北）'})
            SET a.visit_tip = '建议参观振成楼（八卦布局）和承启楼（土楼王），感受不同土楼建筑智慧'
        """)

        # 10. 补充红色旅游提示
         session.run("""
            MATCH (c:City {name: '龙岩'})
            SET c.red_tourism = '闽西革命老区，除古田会议旧址外，可串联参观长汀红色旧址群、才溪乡调查纪念馆'
        """)

        print("龙岩旅游数据导入完成！")

    def import_ningde_data(self):
        """导入宁德市旅游数据"""
        with self.driver.session() as session:
        # 1. 创建城市节点（突出山海特色与产业定位）
         session.run("""
            CREATE 
            (nd:City {
                name: '宁德', 
                level: '四线城市', 
                description: '山海交融，中国大黄鱼之乡，闽东明珠',
                province: '福建省',
                industry_feature: '全球最大的消费类电池生产基地和锂离子电池生产基地，中国锂电之都'
            })
        """)

        # 2. 创建景点节点（强化世界地质公园与摄影属性）
         session.run("""
            CREATE 
            (taimushan:Attraction {
                name: '太姥山', 
                type: '自然景观', 
                rating: 4.6, 
                opening_hours: '7:00 - 17:30',
                honor: '世界地质公园',
                feature: '以花岗岩峰林地貌和海蚀景观闻名'
            }),
            (xiaputantu:Attraction {
                name: '霞浦滩涂', 
                type: '自然景观', 
                rating: 4.5, 
                opening_hours: '全天开放 (最佳观赏时间为早晚)',
                feature: '中国最美滩涂，摄影爱好者天堂'
            })
        """)

        # 3. 创建美食、住宿、交通节点（突出海鲜与摄影主题）
         session.run("""
            CREATE 
            (ningdehuangyu:Food {
                name: '宁德大黄鱼', 
                type: '地方海鲜', 
                price_range: '中高', 
                description: '肉质蒜瓣状，细嫩鲜美，清蒸为上',
                honor: '中国大黄鱼之乡核心特产'
            }),
            (fudingroupian:Food {
                name: '福鼎肉片', 
                type: '地方小吃', 
                price_range: '低', 
                description: '肉质Q弹，汤味酸辣开胃'
            }),

            (ningdewanda:Accommodation {
                name: '宁德万达嘉华酒店', 
                type: '五星级酒店', 
                price_range: '中高', 
                rating: 4.5
            }),
            (xiapushijianhai:Accommodation {
                name: '霞浦拾间海民宿', 
                type: '特色民宿', 
                price_range: '中', 
                rating: 4.7,
                feature: '近滩涂景区，摄影观景绝佳位置'
            }),

            (ningdezhan:Transportation {
                name: '宁德站', 
                type: '高铁站', 
                route: '温福高铁沿线', 
                price: '按里程计费'
            }),
            (ningdegongjiao:Transportation {
                name: '宁德公交', 
                type: '公交', 
                route: '覆盖市区', 
                price: '1-2元'
            })
        """)

        # 4. 创建关系：景点→城市
         session.run("""
            MATCH (a:Attraction), (c:City {name: '宁德'})
            WHERE a.name IN ['太姥山', '霞浦滩涂']
            CREATE (a)-[:LOCATED_IN]->(c)
        """)

        # 5. 创建关系：城市→推荐美食
         session.run("""
            MATCH (c:City {name: '宁德'}), (f:Food)
            WHERE f.name IN ['宁德大黄鱼', '福鼎肉片']
            CREATE (c)-[:RECOMMENDS_FOOD]->(f)
        """)

        # 6. 创建关系：景点→附近美食（结合山海饮食场景）
         session.run("""
            MATCH (a:Attraction {name: '霞浦滩涂'}), (f:Food {name: '宁德大黄鱼'})
            CREATE (a)-[:NEAR_FOOD {distance: '5km', note: '海边餐馆清蒸现捕大黄鱼为特色'}]->(f)
        """)
         session.run("""
            MATCH (a:Attraction {name: '太姥山'}), (f:Food {name: '福鼎肉片'})
            CREATE (a)-[:NEAR_FOOD {distance: '8km', note: '景区周边小吃摊必尝酸辣风味'}]->(f)
        """)

        # 7. 创建关系：景点→附近住宿（匹配摄影与观光需求）
         session.run("""
            MATCH (a:Attraction {name: '霞浦滩涂'}), (ac:Accommodation {name: '霞浦拾间海民宿'})
            CREATE (a)-[:NEAR_ACCOMMODATION {distance: '1km', note: '步行可达滩涂，方便早晚摄影取景'}]->(ac)
        """)
         session.run("""
            MATCH (a:Attraction {name: '太姥山'}), (ac:Accommodation {name: '宁德万达嘉华酒店'})
            CREATE (a)-[:NEAR_ACCOMMODATION {distance: '60km', note: '市区高端酒店，适合多景点串联行程'}]->(ac)
        """)

        # 8. 创建关系：城市→交通及关联
         session.run("""
            MATCH (c:City {name: '宁德'}), (t:Transportation)
            WHERE t.name IN ['宁德站', '宁德公交']
            CREATE (c)-[:HAS_TRANSPORTATION]->(t)
        """)

        # 9. 补充霞浦摄影提示
         session.run("""
            MATCH (a:Attraction {name: '霞浦滩涂'})
            SET a.photography_tip = '最佳拍摄点：北岐、杨家溪、东壁；建议搭配日出日落时段，光影效果最佳'
        """)

        # 10. 补充大黄鱼产业提示
         session.run("""
            MATCH (c:City {name: '宁德'})
            SET c.seafood_industry = '中国最大大黄鱼养殖基地，可参观现代化养殖基地，体验捕捞乐趣'
        """)

        print("宁德旅游数据导入完成！")

    def import_fuqing_data(self):
        """导入福清市旅游数据"""
        with self.driver.session() as session:
        # 1. 创建城市节点（标注县级市代管关系与侨乡属性）
         session.run("""
            CREATE 
            (fq:City {
                name: '福清', 
                level: '县级市（由福州市代管）', 
                description: '著名侨乡，海滨邹鲁，产业新城',
                province: '福建省',
                cultural_feature: '全国著名侨乡，海外侨胞众多，侨乡文化浓厚'
            })
        """)

        # 2. 创建景点节点（突出自然与人文融合属性）
         session.run("""
            CREATE 
            (shizhushan:Attraction {
                name: '石竹山', 
                type: '自然+人文景观', 
                rating: 4.5, 
                opening_hours: '8:00 - 17:00',
                feature: '山清水秀，兼具道教文化与自然风光'
            }),
            (mileiyan:Attraction {
                name: '弥勒岩', 
                type: '人文景观', 
                rating: 4.3, 
                opening_hours: '8:30 - 17:00',
                feature: '巨型弥勒石造像为核心，历史文化底蕴深厚'
            })
        """)

        # 3. 创建美食、住宿、交通节点（突出地方小吃特色）
         session.run("""
            CREATE 
            (fuqingguangbing:Food {
                name: '福清光饼', 
                type: '地方小吃', 
                price_range: '低', 
                description: '酥脆咸香，可夹食蛎饼、红糟肉等',
                feature: '承载历史记忆的标志性小吃，吃法多样'
            }),
            (haixianmenshufen:Food {
                name: '海鲜焖薯粉', 
                type: '地方菜', 
                price_range: '中', 
                description: '薯粉Q弹，海鲜丰富，汤汁浓郁'
            }),

            (chuangyuanqianxi:Accommodation {
                name: '福清创元千禧大酒店', 
                type: '五星级酒店', 
                price_range: '中高', 
                rating: 4.5
            }),
            (jinhuihuayi:Accommodation {
                name: '福清金辉华邑酒店', 
                type: '豪华型酒店', 
                price_range: '中', 
                rating: 4.4
            }),

            (fuqingzhan:Transportation {
                name: '福清站', 
                type: '高铁站', 
                route: '福厦高铁沿线', 
                price: '按里程计费'
            }),
            (fuqinggongjiao:Transportation {
                name: '福清公交', 
                type: '公交', 
                route: '覆盖主城区及乡镇', 
                price: '1-3元'
            })
        """)

        # 4. 创建关系：景点→城市
         session.run("""
            MATCH (a:Attraction), (c:City {name: '福清'})
            WHERE a.name IN ['石竹山', '弥勒岩']
            CREATE (a)-[:LOCATED_IN]->(c)
        """)

        # 5. 创建关系：城市→推荐美食
         session.run("""
            MATCH (c:City {name: '福清'}), (f:Food)
            WHERE f.name IN ['福清光饼', '海鲜焖薯粉']
            CREATE (c)-[:RECOMMENDS_FOOD]->(f)
        """)

        # 6. 创建关系：景点→附近美食（结合场景化饮食需求）
         session.run("""
            MATCH (a:Attraction {name: '弥勒岩'}), (f:Food {name: '福清光饼'})
            CREATE (a)-[:NEAR_FOOD {distance: '1.2km', note: '景区周边小摊可尝现烤光饼'}]->(f)
        """)
         session.run("""
            MATCH (a:Attraction {name: '石竹山'}), (f:Food {name: '海鲜焖薯粉'})
            CREATE (a)-[:NEAR_FOOD {distance: '5km', note: '山脚下餐馆可品海鲜与薯粉融合风味'}]->(f)
        """)

        # 7. 创建关系：景点→附近住宿（匹配城区布局）
         session.run("""
            MATCH (a:Attraction {name: '石竹山'}), (ac:Accommodation {name: '福清创元千禧大酒店'})
            CREATE (a)-[:NEAR_ACCOMMODATION {distance: '8km', note: '城区五星级酒店，设施完善'}]->(ac)
        """)
         session.run("""
            MATCH (a:Attraction {name: '弥勒岩'}), (ac:Accommodation {name: '福清金辉华邑酒店'})
            CREATE (a)-[:NEAR_ACCOMMODATION {distance: '3km', note: '豪华型酒店，出行便利'}]->(ac)
        """)

        # 8. 创建关系：城市→交通及代管与区域关联
         session.run("""
            MATCH (c:City {name: '福清'}), (t:Transportation)
            WHERE t.name IN ['福清站', '福清公交']
            CREATE (c)-[:HAS_TRANSPORTATION]->(t)
        """)
        # 与福州的代管及交通关联
         session.run("""
            MATCH (c1:City {name: '福清'}), (c2:City {name: '福州'})
            CREATE (c1)-[:ADMINISTERED_BY {type: '代管'}]->(c2),
                   (c1)-[:CONNECTED_BY {transport: '福厦高铁', duration: '约20分钟'}]->(c2)
        """)

        # 9. 补充光饼食用提示
         session.run("""
            MATCH (f:Food {name: '福清光饼'})
            SET f.eat_tip = '推荐夹蛎饼、红糟肉或海苔，解锁传统特色吃法'
        """)

        # 10. 补充侨乡文化体验提示
         session.run("""
            MATCH (c:City {name: '福清'})
            SET c.overseas_culture = '可参观侨乡博物馆、百年侨宅，感受侨胞创业与思乡文化'
        """)

        print("福清旅游数据导入完成！")

    def import_yongan_data(self):
        """导入永安市旅游数据"""
        with self.driver.session() as session:
        # 1. 创建城市节点（明确县级市代管关系与产业文化定位）
         session.run("""
            CREATE 
            (ya:City {
                name: '永安', 
                level: '县级市（由三明市代管）', 
                description: '中国笋竹之乡，闽中明珠，抗战文化名城',
                province: '福建省',
                historical_significance: '曾为福建省战时省会，留存丰富抗战文化遗址'
            })
        """)

        # 2. 创建景点节点（强化4A景区与文物保护单位属性）
         session.run("""
            CREATE 
            (taoyuandong:Attraction {
                name: '桃源洞（4A）', 
                type: '自然景观', 
                rating: 4.5, 
                opening_hours: '8:00 - 17:00',
                feature: '以"一线天"奇观闻名，丹霞地貌特色显著'
            }),
            (anzhenbao:Attraction {
                name: '安贞堡（全国重点文物保护单位）', 
                type: '人文景观', 
                rating: 4.6, 
                opening_hours: '8:30 - 17:00',
                feature: '福建现存最完好的古代夯土建筑之一，防御功能突出'
            })
        """)

        # 3. 创建美食、住宿、交通节点（突出笋竹饮食文化）
         session.run("""
            CREATE 
            (yonganguotiao:Food {
                name: '永安粿条', 
                type: '地方小吃', 
                price_range: '低', 
                description: '口感爽滑，汤头鲜美，可搭配活肉/套肠',
                classic_combination: '搭配特制酱油和蒜蓉的"活肉"（猪脸肉等）'
            }),
            (sunzhuyan:Food {
                name: '笋竹宴', 
                type: '地方菜', 
                price_range: '中高', 
                description: '以笋、竹为原料，做法多样，风味独特',
                cultural_tie: '体现"中国笋竹之乡"的食材利用智慧'
            }),

            (wuzhouhotel:Accommodation {
                name: '永安五洲大酒店', 
                type: '四星级酒店', 
                price_range: '中', 
                rating: 4.3
            }),
            (yanjianghotel:Accommodation {
                name: '永安燕江国际酒店', 
                type: '高档型酒店', 
                price_range: '中', 
                rating: 4.2
            }),

            (yonganzhannan:Transportation {
                name: '永安南站', 
                type: '高铁站', 
                route: '南龙铁路沿线', 
                price: '按里程计费'
            }),
            (yongangongjiao:Transportation {
                name: '永安公交', 
                type: '公交', 
                route: '覆盖主城区', 
                price: '1-2元'
            })
        """)

        # 4. 创建关系：景点→城市
         session.run("""
            MATCH (a:Attraction), (c:City {name: '永安'})
            WHERE a.name IN ['桃源洞（4A）', '安贞堡（全国重点文物保护单位）']
            CREATE (a)-[:LOCATED_IN]->(c)
        """)

        # 5. 创建关系：城市→推荐美食
         session.run("""
            MATCH (c:City {name: '永安'}), (f:Food)
            WHERE f.name IN ['永安粿条', '笋竹宴']
            CREATE (c)-[:RECOMMENDS_FOOD]->(f)
        """)

        # 6. 创建关系：景点→附近美食（结合自然与人文场景）
         session.run("""
            MATCH (a:Attraction {name: '桃源洞（4A）'}), (f:Food {name: '永安粿条'})
            CREATE (a)-[:NEAR_FOOD {distance: '3km', note: '景区出口处小吃店可尝经典搭配'}]->(f)
        """)
         session.run("""
            MATCH (a:Attraction {name: '安贞堡（全国重点文物保护单位）'}), (f:Food {name: '笋竹宴'})
            CREATE (a)-[:NEAR_FOOD {distance: '10km', note: '乡镇餐馆可体验全竹宴特色'}]->(f)
        """)

        # 7. 创建关系：景点→附近住宿（匹配城区与景区布局）
         session.run("""
            MATCH (a:Attraction {name: '桃源洞（4A）'}), (ac:Accommodation {name: '永安五洲大酒店'})
            CREATE (a)-[:NEAR_ACCOMMODATION {distance: '5km', note: '城区四星酒店，适合休闲度假'}]->(ac)
        """)
         session.run("""
            MATCH (a:Attraction {name: '安贞堡（全国重点文物保护单位）'}), (ac:Accommodation {name: '永安燕江国际酒店'})
            CREATE (a)-[:NEAR_ACCOMMODATION {distance: '15km', note: '城区高档酒店，方便往返景区'}]->(ac)
        """)

        # 8. 创建关系：城市→交通及代管关联
         session.run("""
            MATCH (c:City {name: '永安'}), (t:Transportation)
            WHERE t.name IN ['永安南站', '永安公交']
            CREATE (c)-[:HAS_TRANSPORTATION]->(t)
        """)
        # 与三明市的代管及交通关联
         session.run("""
            MATCH (c1:City {name: '永安'}), (c2:City {name: '三明'})
            CREATE (c1)-[:ADMINISTERED_BY {type: '代管'}]->(c2),
                   (c1)-[:CONNECTED_BY {transport: '南龙铁路', duration: '约30分钟'}]->(c2)
        """)

        # 9. 补充桃源洞游览提示
         session.run("""
            MATCH (a:Attraction {name: '桃源洞（4A）'})
            SET a.visit_tip = '建议体验"一线天"徒步，最窄处仅容一人通过，需备好手电筒'
        """)

        # 10. 补充抗战文化体验提示
         session.run("""
            MATCH (c:City {name: '永安'})
            SET c.war_history = '可参观永安抗战纪念馆、文庙抗战遗址，了解战时省会历史'
        """)

        print("永安旅游数据导入完成！")

    def import_shishi_data(self):
        """导入石狮市旅游数据"""
        with self.driver.session() as session:
        # 1. 创建城市节点（明确代管关系与核心定位）
         session.run("""
            CREATE 
            (ss:City {
                name: '石狮', 
                level: '县级市（由泉州市代管）', 
                description: '中国服装名城，闽南工贸港口城市，著名侨乡',
                province: '福建省',
                core_feature: '服装产业发达，拥有多个大型服装批发市场，闽南侨乡文化浓厚'
            })
        """)

        # 2. 创建景点节点（强化历史与海滨属性）
         session.run("""
            CREATE 
            (yongninggucheng:Attraction {
                name: '永宁古城', 
                type: '人文景观', 
                rating: 4.4, 
                opening_hours: '全天开放',
                feature: '600多年历史的卫城，留存明清建筑与海防文化遗迹'
            }),
            (huangjinhaian:Attraction {
                name: '黄金海岸', 
                type: '自然景观', 
                rating: 4.2, 
                opening_hours: '全天开放',
                feature: '闽南特色海滨度假区，适合休闲观光、亲子游玩'
            })
        """)

        # 3. 创建美食、住宿、交通节点（突出闽南传统特色）
         session.run("""
            CREATE 
            (shishitianguo:Food {
                name: '石狮甜粿', 
                type: '地方特产', 
                price_range: '中低', 
                description: '糯软香甜，煎食更佳',
                cultural_note: '闽南传统节庆特色糕点，承载侨乡饮食记忆'
            }),
            (yuwan:Food {
                name: '芋丸', 
                type: '地方小吃', 
                price_range: '低', 
                description: '外皮Q弹，内馅咸香'
            }),

            (jianmingguoji:Accommodation {
                name: '石狮建明国际大酒店', 
                type: '五星级酒店', 
                price_range: '中高', 
                rating: 4.5
            }),
            (ailehuangguan:Accommodation {
                name: '石狮爱乐皇冠假日酒店', 
                type: '五星级酒店', 
                price_range: '中高', 
                rating: 4.6
            }),

            (shishizhan:Transportation {
                name: '石狮站', 
                type: '高铁站', 
                route: '福厦高铁沿线', 
                price: '按里程计费'
            }),
            (shishigongjiao:Transportation {
                name: '石狮公交', 
                type: '公交', 
                route: '覆盖全市及主要服装城', 
                price: '1-2元'
            })
        """)

        # 4. 创建关系：景点→城市
         session.run("""
            MATCH (a:Attraction), (c:City {name: '石狮'})
            WHERE a.name IN ['永宁古城', '黄金海岸']
            CREATE (a)-[:LOCATED_IN]->(c)
        """)

        # 5. 创建关系：城市→推荐美食
         session.run("""
            MATCH (c:City {name: '石狮'}), (f:Food)
            WHERE f.name IN ['石狮甜粿', '芋丸']
            CREATE (c)-[:RECOMMENDS_FOOD]->(f)
        """)

        # 6. 创建关系：景点→附近美食（结合场景化体验）
         session.run("""
            MATCH (a:Attraction {name: '永宁古城'}), (f:Food {name: '石狮甜粿'})
            CREATE (a)-[:NEAR_FOOD {distance: '0.5km', note: '古城内老字号店铺可购现做甜粿'}]->(f)
        """)
         session.run("""
            MATCH (a:Attraction {name: '黄金海岸'}), (f:Food {name: '芋丸'})
            CREATE (a)-[:NEAR_FOOD {distance: '1km', note: '海滨大排档现做现吃，搭配海鲜更佳'}]->(f)
        """)

        # 7. 创建关系：景点→附近住宿（匹配商贸与度假需求）
         session.run("""
            MATCH (a:Attraction {name: '永宁古城'}), (ac:Accommodation {name: '石狮建明国际大酒店'})
            CREATE (a)-[:NEAR_ACCOMMODATION {distance: '8km', note: '近服装城，适合商务+旅游兼顾'}]->(ac)
        """)
         session.run("""
            MATCH (a:Attraction {name: '黄金海岸'}), (ac:Accommodation {name: '石狮爱乐皇冠假日酒店'})
            CREATE (a)-[:NEAR_ACCOMMODATION {distance: '5km', note: '高端酒店，度假舒适度高'}]->(ac)
        """)

        # 8. 创建关系：城市→交通及代管关联
         session.run("""
            MATCH (c:City {name: '石狮'}), (t:Transportation)
            WHERE t.name IN ['石狮站', '石狮公交']
            CREATE (c)-[:HAS_TRANSPORTATION]->(t)
        """)
        # 与泉州市的代管及交通联动
         session.run("""
            MATCH (c1:City {name: '石狮'}), (c2:City {name: '泉州'})
            CREATE (c1)-[:ADMINISTERED_BY {type: '代管'}]->(c2),
                   (c1)-[:CONNECTED_BY {transport: '福厦高铁', duration: '约15分钟'}]->(c2)
        """)

        # 9. 补充服装购物提示
         session.run("""
            MATCH (c:City {name: '石狮'})
            SET c.shopping_tip = '推荐前往石狮服装城、国际轻纺城，以批发价选购男装、休闲装等，购物性价比高'
        """)

        # 10. 补充古城游览提示
         session.run("""
            MATCH (a:Attraction {name: '永宁古城'})
            SET a.visit_tip = '建议探访永宁卫碑、城隍庙、古街巷道，感受闽南卫城的历史防御体系与生活气息'
        """)

        print("石狮旅游数据导入完成！")

    def import_jinjiang_data(self):
        """导入晋江市旅游数据"""
        with self.driver.session() as session:
        # 1. 创建城市节点（明确代管关系与核心定位）
         session.run("""
            CREATE 
            (jj:City {
                name: '晋江', 
                level: '县级市（由泉州市代管）', 
                description: '品牌之都，闽南金三角核心，著名侨乡',
                province: '福建省',
                core_feature: '中国鞋都，安踏、特步等知名品牌发源地，侨商经济发达'
            })
        """)

        # 2. 创建景点节点（强化世遗与闽南文化属性）
         session.run("""
            CREATE 
            (wudianshi:Attraction {
                name: '五店市传统街区', 
                type: '人文景观', 
                rating: 4.7, 
                opening_hours: '全天开放 (部分场馆9:00-17:00)',
                feature: '闽南红砖古厝与现代商业融合，体验在地文化的核心区域'
            }),
            (anpingqiao:Attraction {
                name: '安平桥（世遗点）', 
                type: '人文景观', 
                rating: 4.5, 
                opening_hours: '全天开放',
                honor: '世界文化遗产点，中国古代最长的梁式石桥'
            })
        """)

        # 3. 创建美食、住宿、交通节点（突出闽南小吃与交通优势）
         session.run("""
            CREATE 
            (jinjiangniurougeng:Food {
                name: '晋江牛肉羹', 
                type: '地方小吃', 
                price_range: '低', 
                description: '肉质滑嫩，汤底鲜美，常配咸饭',
                scene: '早餐或点心首选，闽南日常饮食代表'
            }),
            (shenhuyuwang:Food {
                name: '深沪鱼丸', 
                type: '地方小吃', 
                price_range: '中低', 
                description: '真材实料，口感Q弹，汤味清甜'
            }),

            (makelubo:Accommodation {
                name: '晋江马哥孛罗酒店', 
                type: '五星级酒店', 
                price_range: '中高', 
                rating: 4.6
            }),
            (baolongdajiudian:Accommodation {
                name: '晋江宝龙大酒店', 
                type: '豪华型酒店', 
                price_range: '中', 
                rating: 4.4
            }),

            (jinjiangzhan:Transportation {
                name: '晋江站', 
                type: '高铁站', 
                route: '福厦高铁沿线', 
                price: '按里程计费'
            }),
            (jinjiangguojijichang:Transportation {
                name: '晋江国际机场', 
                type: '空港', 
                route: '通达国内主要城市', 
                price: '按航班定价'
            })
        """)

        # 4. 创建关系：景点→城市
         session.run("""
            MATCH (a:Attraction), (c:City {name: '晋江'})
            WHERE a.name IN ['五店市传统街区', '安平桥（世遗点）']
            CREATE (a)-[:LOCATED_IN]->(c)
        """)

        # 5. 创建关系：城市→推荐美食
         session.run("""
            MATCH (c:City {name: '晋江'}), (f:Food)
            WHERE f.name IN ['晋江牛肉羹', '深沪鱼丸']
            CREATE (c)-[:RECOMMENDS_FOOD]->(f)
        """)

        # 6. 创建关系：景点→附近美食（结合场景化体验）
         session.run("""
            MATCH (a:Attraction {name: '五店市传统街区'}), (f:Food {name: '晋江牛肉羹'})
            CREATE (a)-[:NEAR_FOOD {distance: '0.3km', note: '街区内及周边遍布老字号小吃店'}]->(f)
        """)
         session.run("""
            MATCH (a:Attraction {name: '安平桥（世遗点）'}), (f:Food {name: '深沪鱼丸'})
            CREATE (a)-[:NEAR_FOOD {distance: '5km', note: '桥周边海鲜餐馆可尝新鲜鱼丸'}]->(f)
        """)

        # 7. 创建关系：景点→附近住宿（匹配商务与旅游需求）
         session.run("""
            MATCH (a:Attraction {name: '五店市传统街区'}), (ac:Accommodation {name: '晋江马哥孛罗酒店'})
            CREATE (a)-[:NEAR_ACCOMMODATION {distance: '2km', note: '高端酒店，兼顾商务与文化游览'}]->(ac)
        """)
         session.run("""
            MATCH (a:Attraction {name: '安平桥（世遗点）'}), (ac:Accommodation {name: '晋江宝龙大酒店'})
            CREATE (a)-[:NEAR_ACCOMMODATION {distance: '8km', note: '豪华型酒店，出行便利'}]->(ac)
        """)

        # 8. 创建关系：城市→交通及代管关联
         session.run("""
            MATCH (c:City {name: '晋江'}), (t:Transportation)
            WHERE t.name IN ['晋江站', '晋江国际机场']
            CREATE (c)-[:HAS_TRANSPORTATION]->(t)
        """)
        # 与泉州市的代管及交通联动
         session.run("""
            MATCH (c1:City {name: '晋江'}), (c2:City {name: '泉州'})
            CREATE (c1)-[:ADMINISTERED_BY {type: '代管'}]->(c2),
                   (c1)-[:CONNECTED_BY {transport: '福厦高铁', duration: '约10分钟'}]->(c2)
        """)

        # 9. 补充品牌购物提示
         session.run("""
            MATCH (c:City {name: '晋江'})
            SET c.shopping_tip = '推荐前往安踏、特步等品牌工厂店或晋江国际鞋纺城，选购高性价比运动服饰与鞋类'
        """)

        # 10. 补充五店市游览提示
         session.run("""
            MATCH (a:Attraction {name: '五店市传统街区'})
            SET a.visit_tip = '建议夜游感受红砖古厝灯光秀，同时体验闽南民俗表演与文创市集'
        """)

        print("晋江旅游数据导入完成！")

    def import_nanan_data(self):
        """导入南安市旅游数据"""
        with self.driver.session() as session:
        # 1. 创建城市节点（明确代管关系与核心定位）
         session.run("""
            CREATE 
            (na:City {
                name: '南安', 
                level: '县级市（由泉州市代管）', 
                description: '海滨邹鲁，民族英雄郑成功故里，中国建材之乡',
                province: '福建省',
                core_feature: '中国石材城，郑成功文化发源地，著名侨乡，石材陶瓷产业全球知名'
            })
        """)

        # 2. 创建景点节点（强化历史人文与名人属性）
         session.run("""
            CREATE 
            (zhenggongcheng:Attraction {
                name: '郑成功文化旅游区', 
                type: '人文景观', 
                rating: 4.6, 
                opening_hours: '8:30 - 17:30',
                feature: '含郑成功纪念馆、陵墓等，展现民族英雄生平与抗清复台历史'
            }),
            (caishiguminju:Attraction {
                name: '蔡氏古民居建筑群', 
                type: '人文景观', 
                rating: 4.5, 
                opening_hours: '8:30 - 17:00',
                feature: '闽南红砖建筑群代表，融合中西建筑风格，被誉为"闽南建筑大观园"'
            })
        """)

        # 3. 创建美食、住宿、交通节点（突出闽南特色小吃）
         session.run("""
            CREATE 
            (honglaijizhua:Food {
                name: '洪濑鸡爪', 
                type: '地方小吃', 
                price_range: '低', 
                description: '卤香入味，皮质Q弹，远近闻名',
                feature: '闽南卤味代表，真空包装便于携带'
            }),
            (guanqiaoshaorouzong:Food {
                name: '官桥烧肉粽', 
                type: '地方小吃', 
                price_range: '低', 
                description: '用料丰富，糯米软糯，油润不腻'
            }),

            (chenggongdajiudian:Accommodation {
                name: '南安成功大酒店', 
                type: '四星级酒店', 
                price_range: '中', 
                rating: 4.3
            }),
            (fanhua:Accommodation {
                name: '南安泛华大酒店', 
                type: '豪华型酒店', 
                price_range: '中', 
                rating: 4.4
            }),

            (nananzhan:Transportation {
                name: '南安站', 
                type: '高铁站', 
                route: '福厦高铁沿线', 
                price: '按里程计费'
            }),
            (nanangongjiao:Transportation {
                name: '南安公交', 
                type: '公交', 
                route: '覆盖主城区及乡镇', 
                price: '1-3元'
            })
        """)

        # 4. 创建关系：景点→城市
         session.run("""
            MATCH (a:Attraction), (c:City {name: '南安'})
            WHERE a.name IN ['郑成功文化旅游区', '蔡氏古民居建筑群']
            CREATE (a)-[:LOCATED_IN]->(c)
        """)

        # 5. 创建关系：城市→推荐美食
         session.run("""
            MATCH (c:City {name: '南安'}), (f:Food)
            WHERE f.name IN ['洪濑鸡爪', '官桥烧肉粽']
            CREATE (c)-[:RECOMMENDS_FOOD]->(f)
        """)

        # 6. 创建关系：景点→附近美食（结合历史与地域场景）
         session.run("""
            MATCH (a:Attraction {name: '郑成功文化旅游区'}), (f:Food {name: '洪濑鸡爪'})
            CREATE (a)-[:NEAR_FOOD {distance: '12km', note: '洪濑镇老字号卤味店可购正宗产品'}]->(f)
        """)
         session.run("""
            MATCH (a:Attraction {name: '蔡氏古民居建筑群'}), (f:Food {name: '官桥烧肉粽'})
            CREATE (a)-[:NEAR_FOOD {distance: '3km', note: '官桥镇街头小吃摊现做现卖'}]->(f)
        """)

        # 7. 创建关系：景点→附近住宿（匹配城区与景区布局）
         session.run("""
            MATCH (a:Attraction {name: '郑成功文化旅游区'}), (ac:Accommodation {name: '南安成功大酒店'})
            CREATE (a)-[:NEAR_ACCOMMODATION {distance: '8km', note: '以郑成功命名，文化主题鲜明'}]->(ac)
        """)
         session.run("""
            MATCH (a:Attraction {name: '蔡氏古民居建筑群'}), (ac:Accommodation {name: '南安泛华大酒店'})
            CREATE (a)-[:NEAR_ACCOMMODATION {distance: '10km', note: '城区豪华酒店，设施完善'}]->(ac)
        """)

        # 8. 创建关系：城市→交通及代管关联
         session.run("""
            MATCH (c:City {name: '南安'}), (t:Transportation)
            WHERE t.name IN ['南安站', '南安公交']
            CREATE (c)-[:HAS_TRANSPORTATION]->(t)
        """)
        # 与泉州市的代管及交通联动
         session.run("""
            MATCH (c1:City {name: '南安'}), (c2:City {name: '泉州'})
            CREATE (c1)-[:ADMINISTERED_BY {type: '代管'}]->(c2),
                   (c1)-[:CONNECTED_BY {transport: '福厦高铁', duration: '约20分钟'}]->(c2)
        """)

        # 9. 补充产业体验提示
         session.run("""
            MATCH (c:City {name: '南安'})
            SET c.industry_experience = '可参观石材博物馆、大型石材市场，了解全球建材产业供应链'
        """)

        # 10. 补充文化游览提示
         session.run("""
            MATCH (a:Attraction {name: '郑成功文化旅游区'})
            SET a.visit_tip = '建议结合讲解了解郑成功抗清复台历史，景区内有传统武术表演可观赏'
        """)

        print("南安旅游数据导入完成！")

    def import_shaowu_data(self):
        """导入邵武市旅游数据"""
        with self.driver.session() as session:
        # 1. 创建城市节点（明确代管关系与核心定位）
         session.run("""
            CREATE 
            (sw:City {
                name: '邵武', 
                level: '县级市（由南平市代管）', 
                description: '闽北林海粮仓，武夷林区名城，黄氏峭公后裔祖地',
                province: '福建省',
                core_feature: '闽北重要商品粮基地与林产加工中心，和平古镇为福建历史最悠久古镇之一'
            })
        """)

        # 2. 创建景点节点（强化自然奇观与古镇历史属性）
         session.run("""
            CREATE 
            (tianchengqixia:Attraction {
                name: '天成奇峡', 
                type: '自然景观', 
                rating: 4.4, 
                opening_hours: '8:00 - 17:00',
                feature: '以丹霞地貌、幽深峡谷为特色，兼具漂流与徒步体验'
            }),
            (hepingguzhen:Attraction {
                name: '和平古镇', 
                type: '人文景观', 
                rating: 4.5, 
                opening_hours: '8:30 - 17:00',
                honor: '中国进士之乡，保留完整古城墙与明清古街',
                feature: '福建历史最悠久古镇之一，科举文化与建筑艺术并存'
            })
        """)

        # 3. 创建美食、住宿、交通节点（突出闽北传统小吃）
         session.run("""
            CREATE 
            (hepingyoujiangdoufu:Food {
                name: '和平游浆豆腐', 
                type: '地方小吃', 
                price_range: '低', 
                description: '古法酿制，豆香浓郁，鲜嫩爽口',
                cultural_tie: '和平古镇特产，传承数百年制作工艺'
            }),
            (baoci:Food {
                name: '包糍', 
                type: '地方小吃', 
                price_range: '低', 
                description: '外皮软糯，馅料丰富，特色米食'
            }),

            (xichunhuameida:Accommodation {
                name: '邵武熙春华美达广场酒店', 
                type: '高档型酒店', 
                price_range: '中', 
                rating: 4.4
            }),
            (wanjia:Accommodation {
                name: '邵武万佳国际酒店', 
                type: '商务型酒店', 
                price_range: '中', 
                rating: 4.2
            }),

            (shaowuzhan:Transportation {
                name: '邵武站', 
                type: '火车站', 
                route: '鹰厦铁路沿线', 
                price: '按里程计费'
            }),
            (shaowugongjiao:Transportation {
                name: '邵武公交', 
                type: '公交', 
                route: '覆盖主城区', 
                price: '1-2元'
            })
        """)

        # 4. 创建关系：景点→城市
         session.run("""
            MATCH (a:Attraction), (c:City {name: '邵武'})
            WHERE a.name IN ['天成奇峡', '和平古镇']
            CREATE (a)-[:LOCATED_IN]->(c)
        """)

        # 5. 创建关系：城市→推荐美食
         session.run("""
            MATCH (c:City {name: '邵武'}), (f:Food)
            WHERE f.name IN ['和平游浆豆腐', '包糍']
            CREATE (c)-[:RECOMMENDS_FOOD]->(f)
        """)

        # 6. 创建关系：景点→附近美食（结合古镇与自然场景）
         session.run("""
            MATCH (a:Attraction {name: '和平古镇'}), (f:Food {name: '和平游浆豆腐'})
            CREATE (a)-[:NEAR_FOOD {distance: '0.2km', note: '古镇内多家作坊可现做现尝，可购真空包装' }]->(f)
        """)
         session.run("""
            MATCH (a:Attraction {name: '天成奇峡'}), (f:Food {name: '包糍'})
            CREATE (a)-[:NEAR_FOOD {distance: '15km', note: '市区及景区周边餐馆早餐常见' }]->(f)
        """)

        # 7. 创建关系：景点→附近住宿（匹配城区与景区布局）
         session.run("""
            MATCH (a:Attraction {name: '和平古镇'}), (ac:Accommodation {name: '邵武熙春华美达广场酒店'})
            CREATE (a)-[:NEAR_ACCOMMODATION {distance: '18km', note: '城区高档酒店，适合休闲度假' }]->(ac)
        """)
         session.run("""
            MATCH (a:Attraction {name: '天成奇峡'}), (ac:Accommodation {name: '邵武万佳国际酒店'})
            CREATE (a)-[:NEAR_ACCOMMODATION {distance: '25km', note: '商务型酒店，交通便利' }]->(ac)
        """)

        # 8. 创建关系：城市→交通及代管关联
         session.run("""
            MATCH (c:City {name: '邵武'}), (t:Transportation)
            WHERE t.name IN ['邵武站', '邵武公交']
            CREATE (c)-[:HAS_TRANSPORTATION]->(t)
        """)
        # 与南平市的代管及交通联动
         session.run("""
            MATCH (c1:City {name: '邵武'}), (c2:City {name: '南平'})
            CREATE (c1)-[:ADMINISTERED_BY {type: '代管'}]->(c2),
                   (c1)-[:CONNECTED_BY {transport: '鹰厦铁路+公路', duration: '约1.5小时'}]->(c2)
        """)

        # 9. 补充林业特色提示
         session.run("""
            MATCH (c:City {name: '邵武'})
            SET c.forestry_feature = '可参观林产加工园区、林海景观带，体验闽北林业文化与生态资源'
        """)

        # 10. 补充古镇游览提示
         session.run("""
            MATCH (a:Attraction {name: '和平古镇'})
            SET a.visit_tip = '建议重点参观大夫第、和平书院，感受科举文化；古街中段的豆腐作坊可体验制作'
        """)

        print("邵武旅游数据导入完成！")

    def import_wuyishan_data(self):
        """导入武夷山市旅游数据"""
        with self.driver.session() as session:
        # 1. 创建城市节点（明确代管关系与核心定位）
         session.run("""
            CREATE 
            (wys:City {
                name: '武夷山', 
                level: '县级市（由南平市代管）', 
                description: '世界双遗产地，中国茶之乡，朱子理学摇篮',
                province: '福建省',
                core_feature: '拥有世界文化与自然双遗产，武夷岩茶（大红袍）原产地，朱子理学发源地'
            })
        """)

        # 2. 创建景点节点（强化世界遗产与文化属性）
         session.run("""
            CREATE 
            (wuyishanfengjingqu:Attraction {
                name: '武夷山风景名胜区（世界文化与自然遗产）', 
                type: '自然+人文景观', 
                rating: 4.8, 
                opening_hours: '7:30 - 17:30 (各景点略有不同)',
                feature: '含天游峰、九曲溪、大红袍等子景点，自然与人文景观融合的世界遗产'
            }),
            (xiamieguminju:Attraction {
                name: '下梅古民居', 
                type: '人文景观', 
                rating: 4.4, 
                opening_hours: '7:30 - 17:30',
                feature: '明清古村落，曾是武夷岩茶外销的重要集散地，保留完整商帮文化遗迹'
            })
        """)

        # 3. 创建美食、住宿、交通节点（突出茶乡特色与旅游配套）
         session.run("""
            CREATE 
            (languxune:Food {
                name: '岚谷熏鹅', 
                type: '地方特色', 
                price_range: '中', 
                description: '色泽金黄，烟香浓郁，肉质紧实',
                origin: '源自武夷山市岚谷乡，传统熏制工艺传承百年'
            }),
            (wengongcai:Food {
                name: '文公菜', 
                type: '地方菜', 
                price_range: '中', 
                description: '为纪念朱熹而创，用料讲究，口感丰富',
                cultural_tie: '与朱子理学文化紧密关联，体现当地尊师重道传统'
            }),

            (jiayeshanshe:Accommodation {
                name: '武夷山嘉叶山舍', 
                type: '奢华度假酒店', 
                price_range: '高', 
                rating: 4.8,
                feature: '毗邻景区，茶主题设计，融合自然与禅意'
            }),
            (jiujieshenghuo:Accommodation {
                name: '武夷山旧街森活民宿', 
                type: '特色民宿', 
                price_range: '中', 
                rating: 4.7,
                feature: '位于旧街区，文艺风格，近美食与购物区'
            }),

            (nanpingshizhan:Transportation {
                name: '南平市站', 
                type: '高铁站', 
                route: '合福高铁沿线', 
                price: '按里程计费'
            }),
            (wuyishanjichang:Transportation {
                name: '武夷山机场', 
                type: '空港', 
                route: '通达国内部分城市', 
                price: '按航班定价'
            }),
            (lvyoutourche:Transportation {
                name: '武夷山旅游观光车', 
                type: '景区交通', 
                route: '连接景区各景点', 
                price: '含在联票内'
            })
        """)

        # 4. 创建关系：景点→城市
         session.run("""
            MATCH (a:Attraction), (c:City {name: '武夷山'})
            WHERE a.name IN ['武夷山风景名胜区（世界文化与自然遗产）', '下梅古民居']
            CREATE (a)-[:LOCATED_IN]->(c)
        """)

        # 5. 创建关系：城市→推荐美食
         session.run("""
            MATCH (c:City {name: '武夷山'}), (f:Food)
            WHERE f.name IN ['岚谷熏鹅', '文公菜']
            CREATE (c)-[:RECOMMENDS_FOOD]->(f)
        """)

        # 6. 创建关系：景点→附近美食（结合景区与文化场景）
         session.run("""
            MATCH (a:Attraction {name: '武夷山风景名胜区（世界文化与自然遗产）'}), (f:Food {name: '文公菜'})
            CREATE (a)-[:NEAR_FOOD {distance: '3km', note: '景区周边餐馆多有供应，搭配武夷岩茶更佳' }]->(f)
        """)
         session.run("""
            MATCH (a:Attraction {name: '下梅古民居'}), (f:Food {name: '岚谷熏鹅'})
            CREATE (a)-[:NEAR_FOOD {distance: '12km', note: '市区及古民居周边特产店可购真空包装' }]->(f)
        """)

        # 7. 创建关系：景点→附近住宿（匹配高端度假与特色体验）
         session.run("""
            MATCH (a:Attraction {name: '武夷山风景名胜区（世界文化与自然遗产）'}), (ac:Accommodation {name: '武夷山嘉叶山舍'})
            CREATE (a)-[:NEAR_ACCOMMODATION {distance: '1.5km', note: '景区内奢华度假体验，茶主题沉浸式住宿' }]->(ac)
        """)
         session.run("""
            MATCH (a:Attraction {name: '下梅古民居'}), (ac:Accommodation {name: '武夷山旧街森活民宿'})
            CREATE (a)-[:NEAR_ACCOMMODATION {distance: '8km', note: '城区特色民宿，适合深度体验当地生活' }]->(ac)
        """)

        # 8. 创建关系：城市→交通及代管关联
         session.run("""
            MATCH (c:City {name: '武夷山'}), (t:Transportation)
            WHERE t.name IN ['南平市站', '武夷山机场', '武夷山旅游观光车']
            CREATE (c)-[:HAS_TRANSPORTATION]->(t)
        """)
        # 与南平市的代管及交通联动
         session.run("""
            MATCH (c1:City {name: '武夷山'}), (c2:City {name: '南平'})
            CREATE (c1)-[:ADMINISTERED_BY {type: '代管'}]->(c2),
                   (c1)-[:CONNECTED_BY {transport: '合福高铁+公路', duration: '约40分钟'}]->(c2)
        """)

        # 9. 补充茶文化体验提示
         session.run("""
            MATCH (c:City {name: '武夷山'})
            SET c.tea_culture = '推荐参观大红袍母树、茶博园，体验采茶制茶工艺，参与茶艺品鉴活动'
        """)

        # 10. 补充景区游览提示
         session.run("""
            MATCH (a:Attraction {name: '武夷山风景名胜区（世界文化与自然遗产）'})
            SET a.visit_tip = '九曲溪竹筏漂流需提前3天预订，天游峰建议早出发避开人流；联票含观光车，有效期多为3天'
        """)

        print("武夷山市旅游数据导入完成！")

    def import_jianou_data(self):
        """导入建瓯市旅游数据"""
        with self.driver.session() as session:
        # 1. 创建城市节点（明确代管关系与核心定位）
         session.run("""
            CREATE 
            (jo:City {
                name: '建瓯', 
                level: '县级市（由南平市代管）', 
                description: '福建最早建县地，中国笋竹城，根艺之都',
                province: '福建省',
                core_feature: '福建历史上最早设置的四县之一，八闽文化发源地之一，笋竹产业与根艺文化突出'
            })
        """)

        # 2. 创建景点节点（强化历史人文与自然融合属性）
         session.run("""
            CREATE 
            (guizongyan:Attraction {
                name: '归宗岩', 
                type: '自然+人文景观', 
                rating: 4.3, 
                opening_hours: '8:00 - 17:00',
                feature: '素有"小武夷"之称，集丹霞地貌与古刹禅意于一体'
            }),
            (jianningfukongmiao:Attraction {
                name: '建宁府孔庙', 
                type: '人文景观', 
                rating: 4.4, 
                opening_hours: '9:00 - 17:00',
                honor: '八闽现存府级孔庙之冠，保留完整儒家祭祀建筑体系'
            })
        """)

        # 3. 创建美食、住宿、交通节点（突出地方特色与产业关联）
         session.run("""
            CREATE 
            (jianouguangbing:Food {
                name: '建瓯光饼', 
                type: '地方小吃', 
                price_range: '低', 
                description: '酥脆咸香，可夹肉、菜等食用',
                history: '源于抗倭历史，传承数百年的街头美食'
            }),
            (jianoubanya:Food {
                name: '建瓯板鸭', 
                type: '地方特产', 
                price_range: '中低', 
                description: '肉质紧实，腊香醇厚',
                feature: '传统腊制工艺，真空包装便于携带'
            }),

            (yinxiangxiaocheng:Accommodation {
                name: '建瓯印象小城大酒店', 
                type: '高档型酒店', 
                price_range: '中', 
                rating: 4.2
            }),
            (wuyibinguan:Accommodation {
                name: '建瓯武夷宾馆', 
                type: '商务型酒店', 
                price_range: '中低', 
                rating: 4.1
            }),

            (jianouxi:Transportation {
                name: '建瓯西站', 
                type: '高铁站', 
                route: '合福高铁沿线', 
                price: '按里程计费'
            }),
            (jianougongjiao:Transportation {
                name: '建瓯公交', 
                type: '公交', 
                route: '覆盖主城区', 
                price: '1-2元'
            })
        """)

        # 4. 创建关系：景点→城市
         session.run("""
            MATCH (a:Attraction), (c:City {name: '建瓯'})
            WHERE a.name IN ['归宗岩', '建宁府孔庙']
            CREATE (a)-[:LOCATED_IN]->(c)
        """)

        # 5. 创建关系：城市→推荐美食
         session.run("""
            MATCH (c:City {name: '建瓯'}), (f:Food)
            WHERE f.name IN ['建瓯光饼', '建瓯板鸭']
            CREATE (c)-[:RECOMMENDS_FOOD]->(f)
        """)

        # 6. 创建关系：景点→附近美食（结合历史与地域场景）
         session.run("""
            MATCH (a:Attraction {name: '建宁府孔庙'}), (f:Food {name: '建瓯光饼'})
            CREATE (a)-[:NEAR_FOOD {distance: '0.8km', note: '孔庙周边老街小摊现烤现卖，可夹肉食用' }]->(f)
        """)
         session.run("""
            MATCH (a:Attraction {name: '归宗岩'}), (f:Food {name: '建瓯板鸭'})
            CREATE (a)-[:NEAR_FOOD {distance: '10km', note: '市区特产店可购，景区餐馆可加工品尝' }]->(f)
        """)

        # 7. 创建关系：景点→附近住宿（匹配城区与景区布局）
         session.run("""
            MATCH (a:Attraction {name: '建宁府孔庙'}), (ac:Accommodation {name: '建瓯印象小城大酒店'})
            CREATE (a)-[:NEAR_ACCOMMODATION {distance: '2km', note: '城区高档酒店，近商圈与文化景点' }]->(ac)
        """)
         session.run("""
            MATCH (a:Attraction {name: '归宗岩'}), (ac:Accommodation {name: '建瓯武夷宾馆'})
            CREATE (a)-[:NEAR_ACCOMMODATION {distance: '12km', note: '商务型酒店，交通便利' }]->(ac)
        """)

        # 8. 创建关系：城市→交通及代管关联
         session.run("""
            MATCH (c:City {name: '建瓯'}), (t:Transportation)
            WHERE t.name IN ['建瓯西站', '建瓯公交']
            CREATE (c)-[:HAS_TRANSPORTATION]->(t)
        """)
        # 与南平市的代管及交通联动
         session.run("""
            MATCH (c1:City {name: '建瓯'}), (c2:City {name: '南平'})
            CREATE (c1)-[:ADMINISTERED_BY {type: '代管'}]->(c2),
                   (c1)-[:CONNECTED_BY {transport: '合福高铁+公路', duration: '约50分钟'}]->(c2)
        """)

        # 9. 补充笋竹产业体验提示
         session.run("""
            MATCH (c:City {name: '建瓯'})
            SET c.bamboo_experience = '可参观笋竹博物馆、竹制品市场，品尝全笋宴，选购根艺品'
        """)

        # 10. 补充历史文化游览提示
         session.run("""
            MATCH (a:Attraction {name: '建宁府孔庙'})
            SET a.visit_tip = '建议参观大成殿、明伦堂，了解闽北儒家文化传承；每月初一、十五有传统祭祀礼仪展示'
        """)

        print("建瓯市旅游数据导入完成！")

    def import_zhangping_data(self):
        """导入漳平市旅游数据"""
        with self.driver.session() as session:
        # 1. 创建城市节点（明确代管关系与核心定位）
         session.run("""
            CREATE 
            (zp:City {
                name: '漳平', 
                level: '县级市（由龙岩市代管）', 
                description: '中国花木之乡，闽西门户，高山茶区',
                province: '福建省',
                core_feature: '漳平水仙茶原产地，永福樱花园、杜鹃花闻名，生态休闲资源丰富'
            })
        """)

        # 2. 创建景点节点（强化生态与茶旅融合属性）
         session.run("""
            CREATE 
            (jiupengxi:Attraction {
                name: '九鹏溪景区', 
                type: '自然景观', 
                rating: 4.4, 
                opening_hours: '8:30 - 17:00',
                feature: '以水上森林、茶山风光为特色，兼具游船观光与徒步体验'
            }),
            (tiantaiguojia:Attraction {
                name: '漳平天台国家森林公园', 
                type: '自然景观', 
                rating: 4.3, 
                opening_hours: '8:00 - 17:00',
                feature: '生态植被茂密，适合森林康养、休闲避暑'
            })
        """)

        # 3. 创建美食、住宿、交通节点（突出茶旅特色与地方小吃）
         session.run("""
            CREATE 
            (zhangpingshuixian:Food {
                name: '漳平水仙茶', 
                type: '地方特产', 
                price_range: '中', 
                description: '乌龙茶类唯一紧压茶，香气清高，滋味甘醇',
                honor: '地理标志产品，南洋镇为核心产区'
            }),
            (qingtangfen:Food {
                name: '清汤粉', 
                type: '地方小吃', 
                price_range: '低', 
                description: '汤头清鲜，米粉爽滑'
            }),

            (shanshuidajiudian:Accommodation {
                name: '漳平山水大酒店', 
                type: '四星级酒店', 
                price_range: '中', 
                rating: 4.2
            }),
            (guolianjiudian:Accommodation {
                name: '漳平国联酒店', 
                type: '商务型酒店', 
                price_range: '中低', 
                rating: 4.1
            }),

            (zhangpingxi:Transportation {
                name: '漳平西站', 
                type: '高铁站', 
                route: '南三龙铁路沿线', 
                price: '按里程计费'
            }),
            (zhangpinggongjiao:Transportation {
                name: '漳平公交', 
                type: '公交', 
                route: '覆盖主城区', 
                price: '1-2元'
            })
        """)

        # 4. 创建关系：景点→城市
         session.run("""
            MATCH (a:Attraction), (c:City {name: '漳平'})
            WHERE a.name IN ['九鹏溪景区', '漳平天台国家森林公园']
            CREATE (a)-[:LOCATED_IN]->(c)
        """)

        # 5. 创建关系：城市→推荐美食
         session.run("""
            MATCH (c:City {name: '漳平'}), (f:Food)
            WHERE f.name IN ['漳平水仙茶', '清汤粉']
            CREATE (c)-[:RECOMMENDS_FOOD]->(f)
        """)

        # 6. 创建关系：景点→附近美食（结合生态与日常场景）
         session.run("""
            MATCH (a:Attraction {name: '九鹏溪景区'}), (f:Food {name: '漳平水仙茶'})
            CREATE (a)-[:NEAR_FOOD {distance: '5km', note: '景区内茶座可品茗，南洋镇茶园可体验制茶' }]->(f)
        """)
         session.run("""
            MATCH (a:Attraction {name: '漳平天台国家森林公园'}), (f:Food {name: '清汤粉'})
            CREATE (a)-[:NEAR_FOOD {distance: '8km', note: '景区出口及市区餐馆早餐常见' }]->(f)
        """)

        # 7. 创建关系：景点→附近住宿（匹配城区与景区布局）
         session.run("""
            MATCH (a:Attraction {name: '九鹏溪景区'}), (ac:Accommodation {name: '漳平山水大酒店'})
            CREATE (a)-[:NEAR_ACCOMMODATION {distance: '20km', note: '城区四星酒店，设施完善' }]->(ac)
        """)
         session.run("""
            MATCH (a:Attraction {name: '漳平天台国家森林公园'}), (ac:Accommodation {name: '漳平国联酒店'})
            CREATE (a)-[:NEAR_ACCOMMODATION {distance: '15km', note: '商务型酒店，交通便利' }]->(ac)
        """)

        # 8. 创建关系：城市→交通及代管关联
         session.run("""
            MATCH (c:City {name: '漳平'}), (t:Transportation)
            WHERE t.name IN ['漳平西站', '漳平公交']
            CREATE (c)-[:HAS_TRANSPORTATION]->(t)
        """)
        # 与龙岩市的代管及交通联动
         session.run("""
            MATCH (c1:City {name: '漳平'}), (c2:City {name: '龙岩'})
            CREATE (c1)-[:ADMINISTERED_BY {type: '代管'}]->(c2),
                   (c1)-[:CONNECTED_BY {transport: '南三龙铁路+公路', duration: '约40分钟'}]->(c2)
        """)

        # 9. 补充花木与茶旅体验提示
         session.run("""
            MATCH (c:City {name: '漳平'})
            SET c.tourism_tip = '春季可前往永福樱花园赏樱、看杜鹃花；南洋镇可参观茶园、体验采茶制茶全流程'
        """)

        # 10. 补充景区游览提示
         session.run("""
            MATCH (a:Attraction {name: '九鹏溪景区'})
            SET a.visit_tip = '建议乘坐游船游览水上森林，沿岸茶山适合拍照；景区内设有茶主题餐厅，可搭配茶点品尝'
        """)

        print("漳平市旅游数据导入完成！")

    def import_fuan_data(self):
        """导入福安旅游数据（修正Cypher语法错误）"""
        with self.driver.session() as session:
            # 1. 创建城市节点（单个语句，多个节点用逗号分隔）
            session.run("""
                CREATE 
                (fa:City {name: '福安', level: '县级市 (由宁德市代管)', description: '中国海峡西岸经济区中心城市之一，中国茶叶之乡，电机电器城'})
            """)

            # 2. 创建景点节点（单个语句）
            session.run("""
                CREATE 
                (baiyunshan:Attraction {name: '白云山', type: '自然景观', rating: 4.5, opening_hours: '8:00 - 17:00'}),
                (liancun:Attraction {name: '廉村', type: '人文景观', rating: 4.4, opening_hours: '全天开放'})
            """)

            # 3. 创建美食、住宿、交通节点（单个语句）
            session.run("""
                CREATE 
                (guangbing:Food {name: '福安光饼', type: '地方小吃', price_range: '低', description: '金黄酥脆，香咸可口'}),
                (muyangkaorou:Food {name: '穆阳烤肉', type: '地方小吃', price_range: '中低', description: '色泽金黄，皮酥肉嫩'}),
                (fuchunhotel:Accommodation {name: '福安富春大酒店', type: '高档型', price_range: '中', rating: 4.3}),
                (dongfanghotel:Accommodation {name: '福安东方大酒店', type: '舒适型', price_range: '中', rating: 4.2}),
                (keyunzhan:Transportation {name: '福安客运站', type: '长途汽车', route: '往返宁德、福州等地', price: '依里程而定'}),
                (fu_an_station:Transportation {name: '福安站', type: '动车', route: '隶属温福铁路', price: '依车次而定'})
            """)

            # 4. 创建关系：景点→城市（单个语句）
            session.run("""
                MATCH (a:Attraction), (c:City {name: '福安'})
                WHERE a.name IN ['白云山', '廉村']
                CREATE (a)-[:LOCATED_IN]->(c)
            """)

            # 5. 创建关系：城市→推荐美食（单个语句，修正冗余关系定义）
            session.run("""
                MATCH (c:City {name: '福安'}), (f:Food)
                WHERE f.name IN ['福安光饼', '穆阳烤肉']
                CREATE (c)-[:RECOMMENDS_FOOD]->(f)
            """)

            # 6. 创建关系：景点→附近美食（单个语句）
            session.run("""
                MATCH (a:Attraction {name: '白云山'}), (f:Food)
                WHERE f.name IN ['福安光饼', '穆阳烤肉']
                CREATE (a)-[:NEAR_FOOD {distance: '5km'}]->(f)
            """)
            session.run("""
                MATCH (a:Attraction {name: '廉村'}), (f:Food)
                WHERE f.name IN ['福安光饼', '穆阳烤肉']
                CREATE (a)-[:NEAR_FOOD {distance: '1.2km'}]->(f)
            """)

            # 7. 可选：创建景点→附近住宿、城市→交通关系（扩展功能）
            session.run("""
                MATCH (a:Attraction {name: '白云山'}), (ac:Accommodation {name: '福安富春大酒店'})
                CREATE (a)-[:NEAR_ACCOMMODATION {distance: '8km'}]->(ac)
            """)
            session.run("""
                MATCH (a:Attraction {name: '廉村'}), (ac:Accommodation {name: '福安东方大酒店'})
                CREATE (a)-[:NEAR_ACCOMMODATION {distance: '3km'}]->(ac)
            """)
            session.run("""
                MATCH (c:City {name: '福安'}), (t:Transportation)
                WHERE t.name IN ['福安客运站', '福安站']
                CREATE (c)-[:HAS_TRANSPORTATION]->(t)
            """)

        print("福安旅游数据导入完成！")

    def import_fuding_data(self):
        """导入福鼎市旅游数据"""
        with self.driver.session() as session:
        # 1. 创建城市节点（明确代管关系与核心定位）
         session.run("""
            CREATE 
            (fd:City {
                name: '福鼎', 
                level: '县级市（由宁德市代管）', 
                description: '中国白茶原产地，闽浙边界商贸城',
                province: '福建省',
                core_feature: '福鼎白茶核心原产地，太姥山世界地质公园（5A）与嵛山岛构成"山海双绝"，闽浙边界商贸重镇'
            })
        """)

        # 2. 创建景点节点（强化世界遗产、5A景区与海岛属性）
         session.run("""
            CREATE 
            (taimushan:Attraction {
                name: '太姥山（世界地质公园, 5A）', 
                type: '自然景观', 
                rating: 4.6, 
                opening_hours: '7:00 - 17:30',
                feature: '以花岗岩峰林、海蚀地貌为核心，融合道教文化遗迹，世界地质公园核心景区'
            }),
            (yushandao:Attraction {
                name: '嵛山岛（中国十大最美海岛之一）', 
                type: '自然景观', 
                rating: 4.5, 
                opening_hours: '全天开放 (需乘船)',
                feature: '拥有海上天湖、高山草甸独特景观，中国十大最美海岛，适合露营与海岛观光'
            })
        """)

        # 3. 创建美食、住宿、交通节点（突出地方小吃与白茶特色）
         session.run("""
            CREATE 
            (fudingroupian:Food {
                name: '福鼎肉片', 
                type: '地方小吃', 
                price_range: '低', 
                description: '肉质Q弹，汤味酸辣开胃，街头霸主',
                feature: '福鼎标志性街头小吃，手工捶打而成，搭配米醋、辣椒风味更佳'
            }),
            (binglangyu:Food {
                name: '槟榔芋', 
                type: '地方特产', 
                price_range: '中低', 
                description: '肉质细腻，香味浓郁，可制作芋泥、芋饺等',
                usage: '多用途食材，蒸、煮、炸、炒皆可，是福鼎宴席与日常饮食常用食材'
            }),

            (jinjiulong:Accommodation {
                name: '福鼎金九龙大酒店', 
                type: '四星级酒店', 
                price_range: '中', 
                rating: 4.4
            }),
            (yuhubinguan:Accommodation {
                name: '太姥山玉湖宾馆', 
                type: '度假酒店', 
                price_range: '中', 
                rating: 4.2,
                feature: '毗邻太姥山景区入口，便于景区游览，度假氛围浓厚'
            }),

            (fudingzhan:Transportation {
                name: '福鼎站', 
                type: '高铁站', 
                route: '温福高铁沿线', 
                price: '按里程计费'
            }),
            (fudingqichezhan:Transportation {
                name: '福鼎汽车站', 
                type: '大巴', 
                route: '通往太姥山、嵛山岛码头等', 
                price: '10-20元'
            })
        """)

        # 4. 创建关系：景点→城市
         session.run("""
            MATCH (a:Attraction), (c:City {name: '福鼎'})
            WHERE a.name IN ['太姥山（世界地质公园, 5A）', '嵛山岛（中国十大最美海岛之一）']
            CREATE (a)-[:LOCATED_IN]->(c)
        """)

        # 5. 创建关系：城市→推荐美食
         session.run("""
            MATCH (c:City {name: '福鼎'}), (f:Food)
            WHERE f.name IN ['福鼎肉片', '槟榔芋']
            CREATE (c)-[:RECOMMENDS_FOOD]->(f)
        """)

        # 6. 创建关系：景点→附近美食（结合山海与日常场景）
         session.run("""
            MATCH (a:Attraction {name: '太姥山（世界地质公园, 5A）'}), (f:Food {name: '福鼎肉片'})
            CREATE (a)-[:NEAR_FOOD {distance: '3km', note: '景区入口处及福鼎市区街头小摊均有售卖，现做现吃' }]->(f)
        """)
         session.run("""
            MATCH (a:Attraction {name: '嵛山岛（中国十大最美海岛之一）'}), (f:Food {name: '槟榔芋'})
            CREATE (a)-[:NEAR_FOOD {distance: '30km', note: '福鼎市区及码头周边特产店可购，餐馆可加工成芋泥、芋饺' }]->(f)
        """)

        # 7. 创建关系：景点→附近住宿（匹配城区与景区布局）
         session.run("""
            MATCH (a:Attraction {name: '太姥山（世界地质公园, 5A）'}), (ac:Accommodation {name: '太姥山玉湖宾馆'})
            CREATE (a)-[:NEAR_ACCOMMODATION {distance: '1km', note: '景区内度假酒店，步行可达景点，游览便利' }]->(ac)
        """)
         session.run("""
            MATCH (a:Attraction {name: '嵛山岛（中国十大最美海岛之一）'}), (ac:Accommodation {name: '福鼎金九龙大酒店'})
            CREATE (a)-[:NEAR_ACCOMMODATION {distance: '35km', note: '城区四星级酒店，设施完善，适合乘船前住宿休整' }]->(ac)
        """)

        # 8. 创建关系：城市→交通及代管关联
         session.run("""
            MATCH (c:City {name: '福鼎'}), (t:Transportation)
            WHERE t.name IN ['福鼎站', '福鼎汽车站']
            CREATE (c)-[:HAS_TRANSPORTATION]->(t)
        """)
        # 与宁德市的代管及交通联动
         session.run("""
            MATCH (c1:City {name: '福鼎'}), (c2:City {name: '宁德'})
            CREATE (c1)-[:ADMINISTERED_BY {type: '代管'}]->(c2),
                   (c1)-[:CONNECTED_BY {transport: '温福高铁+公路', duration: '约1.5小时'}]->(c2)
        """)

        # 9. 补充白茶文化体验提示
         session.run("""
            MATCH (c:City {name: '福鼎'})
            SET c.tea_culture = '推荐前往点头镇参观白茶交易市场、百年茶厂，体验采茶、制茶工艺，选购正宗福鼎白茶'
        """)

        # 10. 补充景区游览提示
         session.run("""
            MATCH (a:Attraction {name: '嵛山岛（中国十大最美海岛之一）'})
            SET a.visit_tip = '需提前查询船班时间（三沙古镇码头/渔井码头乘船），建议预留1-2天深度游览；岛上可露营，需自备或租赁装备'
        """)

        print("福鼎市旅游数据导入完成！")

    def import_beijing_data(self):
        """导入北京旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (bj:City {name: '北京', level: '直辖市', description: '中华人民共和国首都，国家中心城市，世界著名古都'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (forbidden_city:Attraction {name: '故宫', type: '人文景观', rating: 4.9, opening_hours: '8:30 - 17:00 (周一闭馆)'}),
               (great_wall:Attraction {name: '长城', type: '人文景观', rating: 4.8, opening_hours: '6:30 - 19:30 (旺季)'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (roast_duck:Food {name: '北京烤鸭', type: '京菜', price_range: '中高', description: '色泽红润，皮脆肉嫩'}),
               (candied_haws:Food {name: '冰糖葫芦', type: '传统小吃', price_range: '低', description: '酸甜可口，晶莹剔透'}),
               (hilton:Accommodation {name: '北京王府井希尔顿酒店', type: '五星级酒店', price_range: '高', rating: 4.8}),
               (courtyard:Accommodation {name: '北京四合院宾馆', type: '特色民宿', price_range: '中', rating: 4.5}),
               (subway1:Transportation {name: '地铁1号线', type: '地铁', route: '苹果园-环球度假区', price: '3-8元'}),
               (airport_express:Transportation {name: '北京首都国际机场线', type: '机场快轨', route: '东直门-首都机场T2/T3', price: '25元'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '北京'})
               WHERE a.name IN ['故宫', '长城']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '北京'}), (f:Food)
               WHERE f.name IN ['北京烤鸭', '冰糖葫芦']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '故宫'}), (f:Food {name: '北京烤鸭'})
               CREATE (a)-[:NEAR_FOOD {distance: '1km', tip: '王府井大街有多家知名餐厅'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '长城'}), (f:Food {name: '冰糖葫芦'})
               CREATE (a)-[:NEAR_FOOD {distance: '2km', tip: '景区周边有售'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系
            session.run("""
               MATCH (a:Attraction {name: '故宫'}), (ac:Accommodation {name: '北京王府井希尔顿酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '1.5km'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '长城'}), (ac:Accommodation {name: '北京四合院宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '30km'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通之间的换乘关系
            session.run("""
               MATCH (c:City {name: '北京'}), (t:Transportation)
               WHERE t.name IN ['地铁1号线', '北京首都国际机场线']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '地铁1号线'}), (t2:Transportation {name: '北京首都国际机场线'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '便捷换乘'}]->(t2)
           """)

        print("北京旅游数据导入完成！")

    def import_tianjin_data(self):
        """导入天津旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (tj:City {name: '天津', level: '直辖市', description: '国家中心城市，环渤海地区经济中心，北方重要港口城市'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (tianjin_eye:Attraction {name: '天津之眼', type: '人文景观', rating: 4.6, opening_hours: '周二至周日 9:30 - 21:30'}),
               (ancient_street:Attraction {name: '古文化街', type: '人文景观', rating: 4.7, opening_hours: '全天开放'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (goubuli:Food {name: '狗不理包子', type: '津菜', price_range: '中高', description: '鲜而不腻，清香适口'}),
               (jianbing:Food {name: '煎饼果子', type: '天津小吃', price_range: '低', description: '绿豆面薄饼，香脆可口'}),
               (ritz:Accommodation {name: '天津丽思卡尔顿酒店', type: '五星级酒店', price_range: '高', rating: 4.8}),
               (conrad:Accommodation {name: '天津康莱德酒店', type: '五星级酒店', price_range: '高', rating: 4.7}),
               (subway3:Transportation {name: '地铁3号线', type: '地铁', route: '小淀-南站', price: '2-6元'}),
               (airport_bus:Transportation {name: '天津滨海国际机场巴士', type: '机场巴士', route: '机场-天津站', price: '20元'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '天津'})
               WHERE a.name IN ['天津之眼', '古文化街']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '天津'}), (f:Food)
               WHERE f.name IN ['狗不理包子', '煎饼果子']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '天津之眼'}), (f:Food {name: '狗不理包子'})
               CREATE (a)-[:NEAR_FOOD {distance: '2km', tip: '周边商圈有分店'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '古文化街'}), (f:Food {name: '煎饼果子'})
               CREATE (a)-[:NEAR_FOOD {distance: '0.3km', tip: '街区内可品尝正宗口味'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持与前序城市相同的位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '天津之眼'}), (ac:Accommodation {name: '天津丽思卡尔顿酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '3km'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '古文化街'}), (ac:Accommodation {name: '天津康莱德酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '2.5km'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通之间的换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '天津'}), (t:Transportation)
               WHERE t.name IN ['地铁3号线', '天津滨海国际机场巴士']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '地铁3号线'}), (t2:Transportation {name: '天津滨海国际机场巴士'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '天津站可换乘'}]->(t2)
           """)

        print("天津旅游数据导入完成！")

    def import_shanghai_data(self):
        """导入上海旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (sh:City {name: '上海', level: '直辖市', description: '国家中心城市，国际经济、金融、贸易、航运、科技创新中心'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (bund:Attraction {name: '外滩', type: '人文景观', rating: 4.8, opening_hours: '全天开放'}),
               (oriental_pearl:Attraction {name: '东方明珠', type: '人文景观', rating: 4.7, opening_hours: '8:00 - 22:00'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (xiaolongbao:Food {name: '小笼包', type: '本帮菜/小吃', price_range: '中低', description: '皮薄馅大，汤汁鲜美'}),
               (shengjian:Food {name: '生煎', type: '上海小吃', price_range: '低', description: '底部酥脆，肉馅鲜嫩'}),
               (mandarin_oriental:Accommodation {name: '上海浦东文华东方酒店', type: '五星级酒店', price_range: '高', rating: 4.8}),
               (w_hotel:Accommodation {name: '上海外滩W酒店', type: '五星级酒店', price_range: '高', rating: 4.7}),
               (subway2:Transportation {name: '地铁2号线', type: '地铁', route: '徐泾东-浦东国际机场', price: '3-10元'}),
               (maglev:Transportation {name: '磁浮列车', type: '磁浮', route: '龙阳路-浦东国际机场', price: '50元'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '上海'})
               WHERE a.name IN ['外滩', '东方明珠']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '上海'}), (f:Food)
               WHERE f.name IN ['小笼包', '生煎']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '外滩'}), (f:Food {name: '小笼包'})
               CREATE (a)-[:NEAR_FOOD {distance: '1.2km', tip: '城隍庙可品尝正宗口味'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '东方明珠'}), (f:Food {name: '生煎'})
               CREATE (a)-[:NEAR_FOOD {distance: '1.5km', tip: '周边老街有多家老店'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '外滩'}), (ac:Accommodation {name: '上海外滩W酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '0.8km'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '东方明珠'}), (ac:Accommodation {name: '上海浦东文华东方酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '2km'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通之间的换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '上海'}), (t:Transportation)
               WHERE t.name IN ['地铁2号线', '磁浮列车']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '地铁2号线'}), (t2:Transportation {name: '磁浮列车'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '龙阳路站可换乘'}]->(t2)
           """)

        print("上海旅游数据导入完成！")

    def import_chongqing_data(self):
        """导入重庆旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (cq:City {name: '重庆', level: '直辖市', description: '国家中心城市，长江上游地区经济中心，山城、雾都'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (hongyadong:Attraction {name: '洪崖洞', type: '人文景观', rating: 4.8, opening_hours: '11:00 - 23:00'}),
               (ciqikou:Attraction {name: '磁器口古镇', type: '人文景观', rating: 4.6, opening_hours: '全天开放'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (hotpot:Food {name: '重庆火锅', type: '川菜', price_range: '中', description: '麻辣鲜香，回味无穷'}),
               (dandanmian:Food {name: '担担面', type: '重庆小吃', price_range: '低', description: '面条劲道，麻辣爽口'}),
               (niccolo:Accommodation {name: '重庆尼依格罗酒店', type: '五星级酒店', price_range: '高', rating: 4.7}),
               (westin:Accommodation {name: '重庆解放碑威斯汀酒店', type: '五星级酒店', price_range: '高', rating: 4.6}),
               (rail2:Transportation {name: '轨道交通2号线', type: '单轨', route: '较场口-鱼洞', price: '2-7元'}),
               (yangtze_cableway:Transportation {name: '长江索道', type: '索道交通', route: '新华路-上新街', price: '20-30元'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '重庆'})
               WHERE a.name IN ['洪崖洞', '磁器口古镇']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '重庆'}), (f:Food)
               WHERE f.name IN ['重庆火锅', '担担面']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '洪崖洞'}), (f:Food {name: '重庆火锅'})
               CREATE (a)-[:NEAR_FOOD {distance: '0.5km', tip: '附近火锅店密集，可就近品尝'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '磁器口古镇'}), (f:Food {name: '担担面'})
               CREATE (a)-[:NEAR_FOOD {distance: '0.2km', tip: '古镇内多家老字号店铺'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '洪崖洞'}), (ac:Accommodation {name: '重庆解放碑威斯汀酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '1km'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '磁器口古镇'}), (ac:Accommodation {name: '重庆尼依格罗酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '8km'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通特色说明（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '重庆'}), (t:Transportation)
               WHERE t.name IN ['轨道交通2号线', '长江索道']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t:Transportation {name: '轨道交通2号线'})
               SET t.feature = '穿楼景观，山城特色交通'
           """)
            session.run("""
               MATCH (t1:Transportation {name: '轨道交通2号线'}), (t2:Transportation {name: '长江索道'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '较场口站可换乘相关线路前往索道站'}]->(t2)
           """)

        print("重庆旅游数据导入完成！")

    def import_shijiazhuang_data(self):
        """导入石家庄旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (sjz:City {name: '石家庄', level: '地级市', description: '河北省省会，华北地区重要中心城市，铁路枢纽'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (zhengding:Attraction {name: '正定古城', type: '人文景观', rating: 4.5, opening_hours: '全天开放'}),
               (zhaozhou_bridge:Attraction {name: '赵州桥', type: '人文景观', rating: 4.6, opening_hours: '8:00 - 18:00'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (donkey_burger:Food {name: '驴肉火烧', type: '河北小吃', price_range: '低', description: '外酥里嫩，肉香浓郁'}),
               (beef_cake:Food {name: '牛肉罩饼', type: '河北小吃', price_range: '低', description: '汤汁鲜美，饼软肉嫩'}),
               (intercontinental:Accommodation {name: '石家庄万达洲际酒店', type: '五星级酒店', price_range: '高', rating: 4.6}),
               (hilton_sjz:Accommodation {name: '石家庄希尔顿酒店', type: '五星级酒店', price_range: '高', rating: 4.5}),
               (subway1_sjz:Transportation {name: '地铁1号线', type: '地铁', route: '西王-福泽', price: '2-5元'}),
               (zhengding_bus:Transportation {name: '正定机场大巴', type: '机场巴士', route: '市区-正定机场', price: '20元'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '石家庄'})
               WHERE a.name IN ['正定古城', '赵州桥']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '石家庄'}), (f:Food)
               WHERE f.name IN ['驴肉火烧', '牛肉罩饼']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '正定古城'}), (f:Food {name: '牛肉罩饼'})
               CREATE (a)-[:NEAR_FOOD {distance: '0.5km', tip: '古城内可品尝特色风味'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '赵州桥'}), (f:Food {name: '驴肉火烧'})
               CREATE (a)-[:NEAR_FOOD {distance: '1km', tip: '景区周边餐馆有售'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '正定古城'}), (ac:Accommodation {name: '石家庄万达洲际酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '15km'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '赵州桥'}), (ac:Accommodation {name: '石家庄希尔顿酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '40km'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通之间的换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '石家庄'}), (t:Transportation)
               WHERE t.name IN ['地铁1号线', '正定机场大巴']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '地铁1号线'}), (t2:Transportation {name: '正定机场大巴'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '市区站点可换乘大巴'}]->(t2)
           """)

        print("石家庄旅游数据导入完成！")

    def import_tangshan_data(self):
        """导入唐山旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (ts:City {name: '唐山', level: '地级市', description: '河北省重要工业城市，北方瓷都，现代化滨海城市'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (qingdongling:Attraction {name: '清东陵', type: '人文景观', rating: 4.6, opening_hours: '8:30 - 17:00'}),
               (nanhu_park:Attraction {name: '南湖公园', type: '自然景观', rating: 4.5, opening_hours: '全天开放'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (honey_candy:Food {name: '蜂蜜麻糖', type: '唐山特产', price_range: '低', description: '香甜酥脆，入口即化'}),
               (wanlixiang_chicken:Food {name: '万里香烧鸡', type: '唐山美食', price_range: '中', description: '肉质鲜嫩，香味浓郁'}),
               (intercontinental_ts:Accommodation {name: '唐山富力洲际酒店', type: '五星级酒店', price_range: '高', rating: 4.6}),
               (shangri_la_ts:Accommodation {name: '唐山香格里拉大酒店', type: '五星级酒店', price_range: '高', rating: 4.5}),
               (tangshan_bus:Transportation {name: '唐山公交', type: '公交', route: '覆盖全市', price: '1-2元'}),
               (sannvhe_bus:Transportation {name: '三女河机场大巴', type: '机场巴士', route: '市区-三女河机场', price: '15元'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '唐山'})
               WHERE a.name IN ['清东陵', '南湖公园']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '唐山'}), (f:Food)
               WHERE f.name IN ['蜂蜜麻糖', '万里香烧鸡']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '南湖公园'}), (f:Food {name: '蜂蜜麻糖'})
               CREATE (a)-[:NEAR_FOOD {distance: '3km', tip: '市区多家特产店有售'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '清东陵'}), (f:Food {name: '万里香烧鸡'})
               CREATE (a)-[:NEAR_FOOD {distance: '25km', tip: '返回市区后可品尝'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '南湖公园'}), (ac:Accommodation {name: '唐山富力洲际酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '4km'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '清东陵'}), (ac:Accommodation {name: '唐山香格里拉大酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '60km'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通之间的换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '唐山'}), (t:Transportation)
               WHERE t.name IN ['唐山公交', '三女河机场大巴']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '唐山公交'}), (t2:Transportation {name: '三女河机场大巴'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '市区公交枢纽可换乘'}]->(t2)
           """)

        print("唐山旅游数据导入完成！")

    def import_handan_data(self):
        """导入邯郸旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (hd:City {name: '邯郸', level: '地级市', description: '国家历史文化名城，成语典故之都，赵文化发祥地'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (congtai:Attraction {name: '丛台公园', type: '人文景观', rating: 4.5, opening_hours: '6:00 - 22:00'}),
               (xiangtangshan:Attraction {name: '响堂山石窟', type: '人文景观', rating: 4.6, opening_hours: '8:00 - 17:30'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (smoked_meat:Food {name: '邯郸熏肉', type: '地方特色', price_range: '中', description: '色泽红亮，香味浓郁'}),
               (donkey_roll:Food {name: '驴肉卷饼', type: '地方小吃', price_range: '低', description: '肉质鲜嫩，饼皮酥脆'}),
               (handan_hotel:Accommodation {name: '邯郸宾馆', type: '四星级酒店', price_range: '中', rating: 4.4}),
               (wandajiahua:Accommodation {name: '邯郸万达嘉华酒店', type: '五星级酒店', price_range: '高', rating: 4.5}),
               (bus_lines:Transportation {name: '公交线路', type: '公交', route: '覆盖主城区', price: '1-2元'}),
               (handan_east:Transportation {name: '邯郸东站', type: '高铁站', route: '通往全国各地', price: '根据里程'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '邯郸'})
               WHERE a.name IN ['丛台公园', '响堂山石窟']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '邯郸'}), (f:Food)
               WHERE f.name IN ['邯郸熏肉', '驴肉卷饼']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '丛台公园'}), (f:Food {name: '驴肉卷饼'})
               CREATE (a)-[:NEAR_FOOD {distance: '0.8km', tip: '公园周边小吃店有售'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '响堂山石窟'}), (f:Food {name: '邯郸熏肉'})
               CREATE (a)-[:NEAR_FOOD {distance: '5km', tip: '景区附近餐馆可品尝'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '丛台公园'}), (ac:Accommodation {name: '邯郸宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '1.2km'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '响堂山石窟'}), (ac:Accommodation {name: '邯郸万达嘉华酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '20km'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通功能说明（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '邯郸'}), (t:Transportation)
               WHERE t.name IN ['公交线路', '邯郸东站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '公交线路'}), (t2:Transportation {name: '邯郸东站'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '公交可直达高铁站'}]->(t2)
           """)

        print("邯郸旅游数据导入完成！")

    def import_qinhuangdao_data(self):
        """导入秦皇岛旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (qhd:City {name: '秦皇岛', level: '地级市', description: '中国著名滨海旅游城市，北方重要港口城市，避暑胜地'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (shanhaiguan:Attraction {name: '山海关', type: '人文景观', rating: 4.7, opening_hours: '7:00 - 18:00'}),
               (beidaihe:Attraction {name: '北戴河', type: '自然景观', rating: 4.6, opening_hours: '全天开放'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (grilled_prawns:Food {name: '烤大虾', type: '海鲜', price_range: '中', description: '鲜嫩多汁，香气扑鼻'}),
               (sitiaobaozi:Food {name: '四条包子', type: '地方小吃', price_range: '低', description: '皮薄馅大，味道鲜美'}),
               (shangri_la_qhd:Accommodation {name: '秦皇岛香格里拉大酒店', type: '五星级酒店', price_range: '高', rating: 4.6}),
               (sheraton_bdh:Accommodation {name: '北戴河华贸喜来登酒店', type: '五星级酒店', price_range: '高', rating: 4.5}),
               (bus34:Transportation {name: '34路公交', type: '旅游专线', route: '山海关-北戴河', price: '2-5元'}),
               (bdh_airport_bus:Transportation {name: '北戴河机场大巴', type: '机场巴士', route: '市区-北戴河机场', price: '20元'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '秦皇岛'})
               WHERE a.name IN ['山海关', '北戴河']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '秦皇岛'}), (f:Food)
               WHERE f.name IN ['烤大虾', '四条包子']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '北戴河'}), (f:Food {name: '烤大虾'})
               CREATE (a)-[:NEAR_FOOD {distance: '1km', tip: '海滨餐厅可品尝新鲜海鲜'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '山海关'}), (f:Food {name: '四条包子'})
               CREATE (a)-[:NEAR_FOOD {distance: '0.5km', tip: '古城内有老字号店铺'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '山海关'}), (ac:Accommodation {name: '秦皇岛香格里拉大酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '15km'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '北戴河'}), (ac:Accommodation {name: '北戴河华贸喜来登酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '2km'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通功能说明（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '秦皇岛'}), (t:Transportation)
               WHERE t.name IN ['34路公交', '北戴河机场大巴']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t:Transportation {name: '34路公交'})
               SET t.feature = '连接主要景点，旅游出行便利'
           """)
            session.run("""
               MATCH (t1:Transportation {name: '34路公交'}), (t2:Transportation {name: '北戴河机场大巴'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '市区站点可换乘机场大巴'}]->(t2)
           """)

        print("秦皇岛旅游数据导入完成！")

    def import_xingtai_data(self):
        """导入邢台旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (xt:City {name: '邢台', level: '地级市', description: '河北省历史文化名城，华北重要节点城市'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (kongshan:Attraction {name: '崆山白云洞', type: '自然景观', rating: 4.5, opening_hours: '8:30 - 17:00'}),
               (daxiagu:Attraction {name: '邢台大峡谷', type: '自然景观', rating: 4.4, opening_hours: '8:00 - 17:30'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (guotie:Food {name: '邢台锅贴', type: '地方小吃', price_range: '低', description: '外脆里嫩，馅料鲜美'}),
               (heijia_jiaozi:Food {name: '黑家饺子', type: '传统美食', price_range: '中低', description: '皮薄馅大，汤汁丰富'}),
               (wanfeng:Accommodation {name: '邢台万峰大酒店', type: '五星级酒店', price_range: '高', rating: 4.5}),
               (chenguang:Accommodation {name: '邢台辰光商务酒店', type: '商务酒店', price_range: '中', rating: 4.3}),
               (xt_bus:Transportation {name: '邢台公交', type: '公交', route: '覆盖市区', price: '1-2元'}),
               (xt_east:Transportation {name: '邢台东站', type: '高铁站', route: '通往主要城市', price: '根据里程'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '邢台'})
               WHERE a.name IN ['崆山白云洞', '邢台大峡谷']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '邢台'}), (f:Food)
               WHERE f.name IN ['邢台锅贴', '黑家饺子']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '崆山白云洞'}), (f:Food {name: '邢台锅贴'})
               CREATE (a)-[:NEAR_FOOD {distance: '3km', tip: '景区附近餐馆可品尝'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '邢台大峡谷'}), (f:Food {name: '黑家饺子'})
               CREATE (a)-[:NEAR_FOOD {distance: '5km', tip: '返回市区途中可品尝'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '崆山白云洞'}), (ac:Accommodation {name: '邢台万峰大酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '40km'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '邢台大峡谷'}), (ac:Accommodation {name: '邢台辰光商务酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '50km'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '邢台'}), (t:Transportation)
               WHERE t.name IN ['邢台公交', '邢台东站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '邢台公交'}), (t2:Transportation {name: '邢台东站'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '多条公交线直达高铁站'}]->(t2)
           """)

        print("邢台旅游数据导入完成！")

    def import_baoding_data(self):
        """导入保定旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (bd:City {name: '保定', level: '地级市', description: '国家历史文化名城，京津冀地区中心城市之一'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (zhili:Attraction {name: '直隶总督署', type: '人文景观', rating: 4.6, opening_hours: '8:30 - 17:30'}),
               (baiyangdian:Attraction {name: '白洋淀', type: '自然景观', rating: 4.7, opening_hours: '8:00 - 18:00'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (lvrouhuoshao:Food {name: '驴肉火烧', type: '传统小吃', price_range: '低', description: '外酥里嫩，肉香四溢'}),
               (baiyunzhang:Food {name: '白运章包子', type: '老字号', price_range: '中低', description: '皮薄馅大，汤汁鲜美'}),
               (zhuozheng:Accommodation {name: '保定卓正国际酒店', type: '五星级酒店', price_range: '高', rating: 4.6}),
               (diangu:Accommodation {name: '保定电谷国际酒店', type: '商务酒店', price_range: '中', rating: 4.4}),
               (bd_bus:Transportation {name: '保定公交', type: '公交', route: '覆盖市区', price: '1-2元'}),
               (bd_east:Transportation {name: '保定东站', type: '高铁站', route: '通往全国各地', price: '根据里程'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '保定'})
               WHERE a.name IN ['直隶总督署', '白洋淀']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '保定'}), (f:Food)
               WHERE f.name IN ['驴肉火烧', '白运章包子']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '直隶总督署'}), (f:Food {name: '驴肉火烧'})
               CREATE (a)-[:NEAR_FOOD {distance: '0.6km', tip: '周边老字号店铺众多'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '白洋淀'}), (f:Food {name: '白运章包子'})
               CREATE (a)-[:NEAR_FOOD {distance: '30km', tip: '返回市区后可品尝正宗口味'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '直隶总督署'}), (ac:Accommodation {name: '保定卓正国际酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '2km'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '白洋淀'}), (ac:Accommodation {name: '保定电谷国际酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '40km'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '保定'}), (t:Transportation)
               WHERE t.name IN ['保定公交', '保定东站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '保定公交'}), (t2:Transportation {name: '保定东站'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '公交快线直达高铁站，车程约30分钟'}]->(t2)
           """)

        print("保定旅游数据导入完成！")

    def import_zhangjiakou_data(self):
        """导入张家口旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (zjk:City {name: '张家口', level: '地级市', description: '2022年冬奥会举办城市之一，京津冀生态涵养区'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (chongli:Attraction {name: '崇礼滑雪场', type: '运动休闲', rating: 4.7, opening_hours: '8:30 - 16:30'}),
               (dajingmen:Attraction {name: '大境门', type: '人文景观', rating: 4.5, opening_hours: '8:00 - 17:30'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (roast_lamb:Food {name: '烤全羊', type: '蒙餐', price_range: '中高', description: '外焦里嫩，风味独特'}),
               (youmian:Food {name: '莜面窝窝', type: '地方主食', price_range: '低', description: '口感劲道，健康营养'}),
               (huayi:Accommodation {name: '张家口容辰华邑酒店', type: '五星级酒店', price_range: '高', rating: 4.6}),
               (taiwu:Accommodation {name: '崇礼太舞滑雪小镇酒店', type: '度假酒店', price_range: '高', rating: 4.7}),
               (zjk_bus:Transportation {name: '张家口公交', type: '公交', route: '覆盖市区', price: '1-2元'}),
               (jingzhang_rail:Transportation {name: '京张高铁', type: '高铁', route: '北京北-张家口', price: '根据里程'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '张家口'})
               WHERE a.name IN ['崇礼滑雪场', '大境门']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '张家口'}), (f:Food)
               WHERE f.name IN ['烤全羊', '莜面窝窝']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '崇礼滑雪场'}), (f:Food {name: '烤全羊'})
               CREATE (a)-[:NEAR_FOOD {distance: '2km', tip: '滑雪后品尝特色美食'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '大境门'}), (f:Food {name: '莜面窝窝'})
               CREATE (a)-[:NEAR_FOOD {distance: '1km', tip: '景区周边餐馆可体验'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '大境门'}), (ac:Accommodation {name: '张家口容辰华邑酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '3km'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '崇礼滑雪场'}), (ac:Accommodation {name: '崇礼太舞滑雪小镇酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '1km', tip: '滑雪度假便捷住宿'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通特色说明（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '张家口'}), (t:Transportation)
               WHERE t.name IN ['张家口公交', '京张高铁']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t:Transportation {name: '京张高铁'})
               SET t.feature = '冬奥会配套交通，北京至张家口约1小时'
           """)
            session.run("""
               MATCH (t1:Transportation {name: '张家口公交'}), (t2:Transportation {name: '京张高铁'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '公交接驳高铁站，方便快捷'}]->(t2)
           """)

        print("张家口旅游数据导入完成！")

    def import_chengde_data(self):
        """导入承德旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (cd:City {name: '承德', level: '地级市', description: '国际旅游城市，清代夏都，世界文化遗产地'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (bishu:Attraction {name: '承德避暑山庄', type: '人文景观', rating: 4.8, opening_hours: '7:00 - 18:00'}),
               (putuo:Attraction {name: '普陀宗乘之庙', type: '人文景观', rating: 4.7, opening_hours: '8:00 - 17:30'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (lvdagun:Food {name: '承德驴打滚', type: '传统小吃', price_range: '低', description: '软糯香甜，豆香浓郁'}),
               (yewei_hotpot:Food {name: '野味火锅', type: '地方特色', price_range: '中', description: '汤鲜味美，食材天然'}),
               (jiahua:Accommodation {name: '承德嘉华国际酒店', type: '五星级酒店', price_range: '高', rating: 4.6}),
               (shanzhuang:Accommodation {name: '承德山庄宾馆', type: '四星级酒店', price_range: '中', rating: 4.4}),
               (cd_bus:Transportation {name: '承德公交', type: '公交', route: '覆盖市区景点', price: '1-2元'}),
               (cd_south:Transportation {name: '承德南站', type: '高铁站', route: '通往北京等地', price: '根据里程'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '承德'})
               WHERE a.name IN ['承德避暑山庄', '普陀宗乘之庙']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '承德'}), (f:Food)
               WHERE f.name IN ['承德驴打滚', '野味火锅']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '承德避暑山庄'}), (f:Food {name: '承德驴打滚'})
               CREATE (a)-[:NEAR_FOOD {distance: '0.8km', tip: '景区周边小吃街可品尝'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '普陀宗乘之庙'}), (f:Food {name: '野味火锅'})
               CREATE (a)-[:NEAR_FOOD {distance: '3km', tip: '附近餐馆有特色火锅'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '承德避暑山庄'}), (ac:Accommodation {name: '承德嘉华国际酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '2km'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '普陀宗乘之庙'}), (ac:Accommodation {name: '承德山庄宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '4km'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '承德'}), (t:Transportation)
               WHERE t.name IN ['承德公交', '承德南站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '承德公交'}), (t2:Transportation {name: '承德南站'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '旅游专线直达高铁站，方便景点往返'}]->(t2)
           """)

        print("承德旅游数据导入完成！")

    def import_cangzhou_data(self):
        """导入沧州旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (cz:City {name: '沧州', level: '地级市', description: '武术之乡，杂技之乡，环渤海地区重要港口城市'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (wuqiao:Attraction {name: '吴桥杂技大世界', type: '人文景观', rating: 4.6, opening_hours: '8:30 - 17:30'}),
               (tie_shizi:Attraction {name: '沧州铁狮子', type: '人文景观', rating: 4.5, opening_hours: '8:00 - 17:00'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (huoguo_ji:Food {name: '沧州火锅鸡', type: '地方特色', price_range: '中', description: '麻辣鲜香，肉质鲜嫩'}),
               (yangchang_tang:Food {name: '羊肠汤', type: '传统小吃', price_range: '低', description: '汤鲜味美，营养丰富'}),
               (jinshi:Accommodation {name: '沧州金狮国际酒店', type: '五星级酒店', price_range: '高', rating: 4.5}),
               (aerkadiya:Accommodation {name: '沧州阿尔卡迪亚国际酒店', type: '五星级酒店', price_range: '高', rating: 4.6}),
               (cz_bus:Transportation {name: '沧州公交', type: '公交', route: '覆盖市区', price: '1-2元'}),
               (cz_west:Transportation {name: '沧州西站', type: '高铁站', route: '通往主要城市', price: '根据里程'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '沧州'})
               WHERE a.name IN ['吴桥杂技大世界', '沧州铁狮子']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '沧州'}), (f:Food)
               WHERE f.name IN ['沧州火锅鸡', '羊肠汤']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '吴桥杂技大世界'}), (f:Food {name: '沧州火锅鸡'})
               CREATE (a)-[:NEAR_FOOD {distance: '5km', tip: '景区周边餐馆可品尝特色火锅鸡'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '沧州铁狮子'}), (f:Food {name: '羊肠汤'})
               CREATE (a)-[:NEAR_FOOD {distance: '2km', tip: '附近老字号店铺有地道风味'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '吴桥杂技大世界'}), (ac:Accommodation {name: '沧州金狮国际酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '50km'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '沧州铁狮子'}), (ac:Accommodation {name: '沧州阿尔卡迪亚国际酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '8km'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '沧州'}), (t:Transportation)
               WHERE t.name IN ['沧州公交', '沧州西站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '沧州公交'}), (t2:Transportation {name: '沧州西站'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '多条公交线直达高铁站，方便快捷'}]->(t2)
           """)

        print("沧州旅游数据导入完成！")

    def import_langfang_data(self):
        """导入廊坊旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (lf:City {name: '廊坊', level: '地级市', description: '京津冀城市群核心区域，京津走廊上的明珠'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (tianxia:Attraction {name: '天下第一城', type: '人文景观', rating: 4.5, opening_hours: '8:30 - 17:00'}),
               (ziran:Attraction {name: '自然公园', type: '自然景观', rating: 4.3, opening_hours: '全天开放'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (xianghe:Food {name: '香河肉饼', type: '地方特色', price_range: '中低', description: '皮薄馅厚，香酥可口'}),
               (sanhe:Food {name: '三河豆片', type: '传统小吃', price_range: '低', description: '豆香浓郁，口感细腻'}),
               (qixiu:Accommodation {name: '廊坊新绎七修酒店', type: '五星级酒店', price_range: '高', rating: 4.6}),
               (guoji:Accommodation {name: '廊坊国际饭店', type: '四星级酒店', price_range: '中', rating: 4.4}),
               (lf_bus:Transportation {name: '廊坊公交', type: '公交', route: '覆盖市区', price: '1-2元'}),
               (lf_rail:Transportation {name: '廊坊站', type: '高铁站', route: '20分钟直达北京', price: '根据里程'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '廊坊'})
               WHERE a.name IN ['天下第一城', '自然公园']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '廊坊'}), (f:Food)
               WHERE f.name IN ['香河肉饼', '三河豆片']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '天下第一城'}), (f:Food {name: '香河肉饼'})
               CREATE (a)-[:NEAR_FOOD {distance: '0.3km', tip: '景区内可品尝地道风味'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '自然公园'}), (f:Food {name: '三河豆片'})
               CREATE (a)-[:NEAR_FOOD {distance: '2km', tip: '公园周边市场有售'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '天下第一城'}), (ac:Accommodation {name: '廊坊新绎七修酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '30km'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '自然公园'}), (ac:Accommodation {name: '廊坊国际饭店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '3km'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通特色说明（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '廊坊'}), (t:Transportation)
               WHERE t.name IN ['廊坊公交', '廊坊站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t:Transportation {name: '廊坊站'})
               SET t.feature = '京津走廊重要站点，20分钟直达北京'
           """)
            session.run("""
               MATCH (t1:Transportation {name: '廊坊公交'}), (t2:Transportation {name: '廊坊站'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '公交直达高铁站，无缝衔接京津'}]->(t2)
           """)

        print("廊坊旅游数据导入完成！")

    def importhengshui_data(self):
        """导入衡水旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (hs:City {name: '衡水', level: '地级市', description: '基础教育教育名城，北方湖城，京津冀重要节点城市'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (hengshui_lake:Attraction {name: '衡水湖', type: '自然景观', rating: 4.6, opening_hours: '8:00 - 18:00'}),
               (baoyun_temple:Attraction {name: '宝云寺', type: '人文景观', rating: 4.4, opening_hours: '8:30 - 17:00'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (fish_banquet:Food {name: '衡水湖全鱼宴', type: '地方特色', price_range: '中高', description: '食材新鲜，烹饪讲究'}),
               (gucheng_smoked_meat:Food {name: '故城熏肉', type: '传统美食', price_range: '中', description: '色泽红亮，风味独特'}),
               (taihua_hotel:Accommodation {name: '衡水泰华温泉酒店', type: '五星级酒店', price_range: '高', rating: 4.5}),
               (yangguang_hotel:Accommodation {name: '衡水阳光大酒店', type: '四星级酒店', price_range: '中', rating: 4.3}),
               (hs_bus:Transportation {name: '衡水公交', type: '公交', route: '覆盖市区', price: '1-2元'}),
               (hs_north:Transportation {name: '衡水北站', type: '高铁站', route: '通往石家庄等地', price: '根据里程'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '衡水'})
               WHERE a.name IN ['衡水湖', '宝云寺']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '衡水'}), (f:Food)
               WHERE f.name IN ['衡水湖全鱼宴', '故城熏肉']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '衡水湖'}), (f:Food {name: '衡水湖全鱼宴'})
               CREATE (a)-[:NEAR_FOOD {distance: '0.5km', tip: '景区内餐馆可品尝新鲜湖鲜'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '宝云寺'}), (f:Food {name: '故城熏肉'})
               CREATE (a)-[:NEAR_FOOD {distance: '3km', tip: '市区老字号店铺有售'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '衡水湖'}), (ac:Accommodation {name: '衡水泰华温泉酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '8km'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '宝云寺'}), (ac:Accommodation {name: '衡水阳光大酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '2km'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '衡水'}), (t:Transportation)
               WHERE t.name IN ['衡水公交', '衡水北站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '衡水公交'}), (t2:Transportation {name: '衡水北站'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '公交专线直达高铁站，方便快捷'}]->(t2)
           """)

        print("衡水旅游数据导入完成！")

    def import_xinji_data(self):
        """导入辛集旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (xj:City {name: '辛集', level: '县级市', description: '中国皮都，北方重要皮革生产基地'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (leather_city:Attraction {name: '辛集国际皮革城', type: '商业旅游', rating: 4.4, opening_hours: '9:00 - 18:00'}),
               (runze_lake:Attraction {name: '润泽湖公园', type: '自然景观', rating: 4.3, opening_hours: '全天开放'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (xinji_chicken:Food {name: '辛集扒鸡', type: '地方特色', price_range: '中低', description: '骨酥肉烂，香味浓郁'}),
               (jinshulu_candy:Food {name: '金束鹿酥糖', type: '传统糕点', price_range: '低', description: '酥脆香甜，入口即化'}),
               (pidu_hotel:Accommodation {name: '辛集皮都国际酒店', type: '四星级酒店', price_range: '中', rating: 4.4}),
               (huayi_hotel:Accommodation {name: '辛集华驿酒店', type: '商务酒店', price_range: '中低', rating: 4.2}),
               (xj_bus:Transportation {name: '辛集公交', type: '公交', route: '覆盖市区', price: '1-2元'}),
               (xj_railway:Transportation {name: '辛集站', type: '火车站', route: '通往石家庄等地', price: '根据里程'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '辛集'})
               WHERE a.name IN ['辛集国际皮革城', '润泽湖公园']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '辛集'}), (f:Food)
               WHERE f.name IN ['辛集扒鸡', '金束鹿酥糖']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '辛集国际皮革城'}), (f:Food {name: '辛集扒鸡'})
               CREATE (a)-[:NEAR_FOOD {distance: '1km', tip: '皮革城周边餐馆可品尝'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '润泽湖公园'}), (f:Food {name: '金束鹿酥糖'})
               CREATE (a)-[:NEAR_FOOD {distance: '1.5km', tip: '公园附近特产店有售'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '辛集国际皮革城'}), (ac:Accommodation {name: '辛集皮都国际酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '0.8km', tip: '皮革主题酒店，购物便利'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '润泽湖公园'}), (ac:Accommodation {name: '辛集华驿酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '2km'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '辛集'}), (t:Transportation)
               WHERE t.name IN ['辛集公交', '辛集站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '辛集公交'}), (t2:Transportation {name: '辛集站'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '多条公交线直达火车站'}]->(t2)
           """)

        print("辛集旅游数据导入完成！")

    def import_jinzhou_data(self):
        """导入晋州旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (jz:City {name: '晋州', level: '县级市', description: '河北省县级市，石家庄代管，传统农业市'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (weizheng_park:Attraction {name: '魏征公园', type: '人文景观', rating: 4.2, opening_hours: '全天开放'}),
               (zhoujiazhuang:Attraction {name: '周家庄农业观光园', type: '乡村休闲', rating: 4.3, opening_hours: '8:00 - 18:00'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (jinzhou_pear:Food {name: '晋州鸭梨', type: '地方特产', price_range: '低', description: '汁多味甜，肉质细腻'}),
               (jinzhou_noodle:Food {name: '晋州烩面', type: '地方小吃', price_range: '低', description: '面条劲道，汤汁浓郁'}),
               (jinzhou_hotel:Accommodation {name: '晋州宾馆', type: '三星级酒店', price_range: '中低', rating: 4.2}),
               (yuecheng_hotel:Accommodation {name: '晋州悦城商务酒店', type: '商务酒店', price_range: '中低', rating: 4.1}),
               (jz_bus:Transportation {name: '晋州公交', type: '公交', route: '覆盖市区', price: '1-2元'}),
               (jz_railway:Transportation {name: '晋州站', type: '火车站', route: '通往石家庄等地', price: '根据里程'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '晋州'})
               WHERE a.name IN ['魏征公园', '周家庄农业观光园']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '晋州'}), (f:Food)
               WHERE f.name IN ['晋州鸭梨', '晋州烩面']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '周家庄农业观光园'}), (f:Food {name: '晋州鸭梨'})
               CREATE (a)-[:NEAR_FOOD {distance: '0.3km', tip: '观光园内可采摘品尝新鲜鸭梨'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '魏征公园'}), (f:Food {name: '晋州烩面'})
               CREATE (a)-[:NEAR_FOOD {distance: '1km', tip: '公园周边餐馆可品尝地道烩面'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '魏征公园'}), (ac:Accommodation {name: '晋州宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '1.5km'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '周家庄农业观光园'}), (ac:Accommodation {name: '晋州悦城商务酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '5km'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '晋州'}), (t:Transportation)
               WHERE t.name IN ['晋州公交', '晋州站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '晋州公交'}), (t2:Transportation {name: '晋州站'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '公交直达火车站，出行便利'}]->(t2)
           """)

        print("晋州旅游数据导入完成！")

    def import_xinle_data(self):
        """导入新乐旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (xl:City {name: '新乐', level: '县级市', description: '河北省县级市，石家庄代管，伏羲文化发祥地'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (fuxitai:Attraction {name: '伏羲台', type: '人文景观', rating: 4.3, opening_hours: '8:30 - 17:30'}),
               (hebei_art_college:Attraction {name: '河北美术学院', type: '人文景观', rating: 4.4, opening_hours: '预约开放'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (xinle_peanut:Food {name: '新乐花生', type: '地方特产', price_range: '低', description: '颗粒饱满，香脆可口'}),
               (xinle_smoked_meat:Food {name: '新乐熏肉', type: '传统美食', price_range: '中低', description: '色泽金黄，风味独特'}),
               (fuxi_hotel:Accommodation {name: '新乐伏羲宾馆', type: '三星级酒店', price_range: '中低', rating: 4.2}),
               (jinzuo_hotel:Accommodation {name: '新乐金座商务酒店', type: '商务酒店', price_range: '中低', rating: 4.1}),
               (xl_bus:Transportation {name: '新乐公交', type: '公交', route: '覆盖市区', price: '1-2元'}),
               (xl_railway:Transportation {name: '新乐站', type: '火车站', route: '通往石家庄等地', price: '根据里程'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '新乐'})
               WHERE a.name IN ['伏羲台', '河北美术学院']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '新乐'}), (f:Food)
               WHERE f.name IN ['新乐花生', '新乐熏肉']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '伏羲台'}), (f:Food {name: '新乐熏肉'})
               CREATE (a)-[:NEAR_FOOD {distance: '2km', tip: '景区周边餐馆可品尝特色熏肉'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '河北美术学院'}), (f:Food {name: '新乐花生'})
               CREATE (a)-[:NEAR_FOOD {distance: '1.5km', tip: '学校周边特产店有售'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '伏羲台'}), (ac:Accommodation {name: '新乐伏羲宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '3km', tip: '毗邻伏羲文化景区，主题特色鲜明'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '河北美术学院'}), (ac:Accommodation {name: '新乐金座商务酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '2km'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '新乐'}), (t:Transportation)
               WHERE t.name IN ['新乐公交', '新乐站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '新乐公交'}), (t2:Transportation {name: '新乐站'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '公交直达火车站，方便往返石家庄'}]->(t2)
           """)

        print("新乐旅游数据导入完成！")

    def import_zunhua_data(self):
        """导入遵化旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (zh:City {name: '遵化', level: '县级市', description: '河北省县级市，唐山代管，清代皇家陵寝所在地'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (qingdongling:Attraction {name: '清东陵', type: '人文景观', rating: 4.7, opening_hours: '8:30 - 17:00'}),
               (tangquangong:Attraction {name: '汤泉宫温泉', type: '休闲度假', rating: 4.5, opening_hours: '9:00 - 21:00'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (zunhua_banli:Food {name: '遵化板栗', type: '地方特产', price_range: '中低', description: '香甜软糯，营养丰富'}),
               (dongling_gaodian:Food {name: '东陵糕点', type: '传统美食', price_range: '低', description: '做工精细，口味独特'}),
               (zunhua_international:Accommodation {name: '遵化国际饭店', type: '四星级酒店', price_range: '中', rating: 4.5}),
               (tangquangong_hotel:Accommodation {name: '汤泉宫温泉酒店', type: '度假酒店', price_range: '中高', rating: 4.4}),
               (zh_bus:Transportation {name: '遵化公交', type: '公交', route: '覆盖市区', price: '1-2元'}),
               (zh_bus_station:Transportation {name: '遵化汽车站', type: '客运站', route: '通往唐山等地', price: '根据里程'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '遵化'})
               WHERE a.name IN ['清东陵', '汤泉宫温泉']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '遵化'}), (f:Food)
               WHERE f.name IN ['遵化板栗', '东陵糕点']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '清东陵'}), (f:Food {name: '东陵糕点'})
               CREATE (a)-[:NEAR_FOOD {distance: '3km', tip: '景区服务区有售传统糕点'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '汤泉宫温泉'}), (f:Food {name: '遵化板栗'})
               CREATE (a)-[:NEAR_FOOD {distance: '2km', tip: '温泉周边特产店可购买'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '清东陵'}), (ac:Accommodation {name: '遵化国际饭店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '25km'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '汤泉宫温泉'}), (ac:Accommodation {name: '汤泉宫温泉酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '0.5km', tip: '温泉配套酒店，休闲便利'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '遵化'}), (t:Transportation)
               WHERE t.name IN ['遵化公交', '遵化汽车站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '遵化公交'}), (t2:Transportation {name: '遵化汽车站'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '公交直达客运站，方便前往唐山市区'}]->(t2)
           """)

        print("遵化旅游数据导入完成！")

    def import_qianan_data(self):
        """导入迁安旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (qa:City {name: '迁安', level: '县级市', description: '河北省县级市，唐山代管，北方水城，钢铁之城'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (huangtaishan:Attraction {name: '黄台山公园', type: '自然景观', rating: 4.4, opening_hours: '全天开放'}),
               (shanyekou:Attraction {name: '山叶口景区', type: '自然景观', rating: 4.5, opening_hours: '8:00 - 17:30'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (qianan_laojiu:Food {name: '迁安老酒', type: '地方特产', price_range: '中', description: '醇厚甘甜，回味悠长'}),
               (jianchangying_sanzi:Food {name: '建昌营馓子', type: '传统小吃', price_range: '低', description: '酥脆可口，老少皆宜'}),
               (jinjiang_hotel:Accommodation {name: '迁安锦江饭店', type: '四星级酒店', price_range: '中', rating: 4.4}),
               (international_hotel:Accommodation {name: '迁安国际酒店', type: '商务酒店', price_range: '中', rating: 4.3}),
               (qa_bus:Transportation {name: '迁安公交', type: '公交', route: '覆盖市区', price: '1-2元'}),
               (qa_railway:Transportation {name: '迁安站', type: '火车站', route: '通往唐山等地', price: '根据里程'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '迁安'})
               WHERE a.name IN ['黄台山公园', '山叶口景区']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '迁安'}), (f:Food)
               WHERE f.name IN ['迁安老酒', '建昌营馓子']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '黄台山公园'}), (f:Food {name: '建昌营馓子'})
               CREATE (a)-[:NEAR_FOOD {distance: '1km', tip: '公园周边小吃街可品尝特色馓子'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '山叶口景区'}), (f:Food {name: '迁安老酒'})
               CREATE (a)-[:NEAR_FOOD {distance: '8km', tip: '景区出口特产店可购买'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '黄台山公园'}), (ac:Accommodation {name: '迁安锦江饭店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '2km'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '山叶口景区'}), (ac:Accommodation {name: '迁安国际酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '20km'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '迁安'}), (t:Transportation)
               WHERE t.name IN ['迁安公交', '迁安站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '迁安公交'}), (t2:Transportation {name: '迁安站'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '公交直达火车站，方便往返唐山'}]->(t2)
           """)

        print("迁安旅游数据导入完成！")

    def import_luanzhou_data(self):
        """导入滦州旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (lz:City {name: '滦州', level: '县级市', description: '河北省县级市，唐山代管，千年古县，滦河文化发祥地'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (luanzhou_oldtown:Attraction {name: '滦州古城', type: '人文景观', rating: 4.5, opening_hours: '全天开放'}),
               (yanshan_scenic:Attraction {name: '研山风景区', type: '自然景观', rating: 4.3, opening_hours: '8:00 - 17:30'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (huasheng_sutang:Food {name: '滦州花生酥糖', type: '地方特产', price_range: '低', description: '酥脆香甜，入口即化'}),
               (luanhe_redcarp:Food {name: '滦河红鲤', type: '地方特色', price_range: '中', description: '肉质鲜嫩，营养丰富'}),
               (gucheng_inn:Accommodation {name: '滦州古城客栈', type: '特色民宿', price_range: '中低', rating: 4.4}),
               (luanzhou_international:Accommodation {name: '滦州国际酒店', type: '商务酒店', price_range: '中', rating: 4.3}),
               (lz_bus:Transportation {name: '滦州公交', type: '公交', route: '覆盖市区', price: '1-2元'}),
               (luanxian_railway:Transportation {name: '滦县站', type: '火车站', route: '通往唐山等地', price: '根据里程'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '滦州'})
               WHERE a.name IN ['滦州古城', '研山风景区']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '滦州'}), (f:Food)
               WHERE f.name IN ['滦州花生酥糖', '滦河红鲤']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '滦州古城'}), (f:Food {name: '滦州花生酥糖'})
               CREATE (a)-[:NEAR_FOOD {distance: '0.2km', tip: '古城内商铺有售传统酥糖'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '滦州古城'}), (f:Food {name: '滦河红鲤'})
               CREATE (a)-[:NEAR_FOOD {distance: '0.5km', tip: '古城周边餐馆可品尝河鲜'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '研山风景区'}), (f:Food {name: '滦州花生酥糖'})
               CREATE (a)-[:NEAR_FOOD {distance: '4km', tip: '返回市区途中可购买特产'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '滦州古城'}), (ac:Accommodation {name: '滦州古城客栈'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '0.3km', tip: '古城内特色住宿，体验浓厚'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '研山风景区'}), (ac:Accommodation {name: '滦州国际酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '5km'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '滦州'}), (t:Transportation)
               WHERE t.name IN ['滦州公交', '滦县站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '滦州公交'}), (t2:Transportation {name: '滦县站'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '公交直达火车站，方便前往唐山、北京'}]->(t2)
           """)

        print("滦州旅游数据导入完成！")

    def import_wuan_data(self):
        """导入武安旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (wa:City {name: '武安', level: '县级市', description: '河北省县级市，邯郸代管，千年古县，钢铁重镇'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (jingnianghu:Attraction {name: '京娘湖', type: '自然景观', rating: 4.6, opening_hours: '8:00 - 17:30'}),
               (guwudangshan:Attraction {name: '古武当山', type: '自然景观', rating: 4.5, opening_hours: '7:30 - 17:00'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (wuan_zhuaimian:Food {name: '武安拽面', type: '地方小吃', price_range: '低', description: '面条筋道，卤汁鲜美'}),
               (wuan_matang:Food {name: '武安小麻糖', type: '传统糕点', price_range: '低', description: '香甜酥脆，风味独特'}),
               (caifu_hotel:Accommodation {name: '武安财富国际酒店', type: '四星级酒店', price_range: '中', rating: 4.4}),
               (yayuan_hotel:Accommodation {name: '武安雅园国际酒店', type: '商务酒店', price_range: '中', rating: 4.3}),
               (wa_bus:Transportation {name: '武安公交', type: '公交', route: '覆盖市区', price: '1-2元'}),
               (wa_railway:Transportation {name: '武安站', type: '火车站', route: '通往邯郸等地', price: '根据里程'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '武安'})
               WHERE a.name IN ['京娘湖', '古武当山']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '武安'}), (f:Food)
               WHERE f.name IN ['武安拽面', '武安小麻糖']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '京娘湖'}), (f:Food {name: '武安拽面'})
               CREATE (a)-[:NEAR_FOOD {distance: '1km', tip: '景区内餐馆可品尝特色拽面'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '古武当山'}), (f:Food {name: '武安小麻糖'})
               CREATE (a)-[:NEAR_FOOD {distance: '5km', tip: '山脚下商铺有售传统糕点'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '京娘湖'}), (ac:Accommodation {name: '武安财富国际酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '30km'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '古武当山'}), (ac:Accommodation {name: '武安雅园国际酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '25km'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '武安'}), (t:Transportation)
               WHERE t.name IN ['武安公交', '武安站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '武安公交'}), (t2:Transportation {name: '武安站'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '公交直达火车站，方便前往邯郸市区'}]->(t2)
           """)

        print("武安旅游数据导入完成！")

    def import_nangong_data(self):
        """导入南宫旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (ng:City {name: '南宫', level: '县级市', description: '河北省县级市，邢台代管，冀南重要商埠'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (nangong_lake:Attraction {name: '南宫湖', type: '自然景观', rating: 4.2, opening_hours: '全天开放'}),
               (putong_temple:Attraction {name: '普彤寺', type: '人文景观', rating: 4.3, opening_hours: '8:00 - 17:00'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (nangong_xuncai:Food {name: '南宫熏菜', type: '地方特色', price_range: '中低', description: '熏香浓郁，风味独特'}),
               (nangong_daguocai:Food {name: '南宫大锅菜', type: '传统美食', price_range: '低', description: '食材丰富，汤汁浓郁'}),
               (nangong_hotel:Accommodation {name: '南宫宾馆', type: '三星级酒店', price_range: '中低', rating: 4.2}),
               (shangkeyou_hotel:Accommodation {name: '南宫尚客优酒店', type: '商务酒店', price_range: '中低', rating: 4.1}),
               (ng_bus:Transportation {name: '南宫公交', type: '公交', route: '覆盖市区', price: '1-2元'}),
               (ng_bus_station:Transportation {name: '南宫汽车站', type: '客运站', route: '通往邢台等地', price: '根据里程'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '南宫'})
               WHERE a.name IN ['南宫湖', '普彤寺']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '南宫'}), (f:Food)
               WHERE f.name IN ['南宫熏菜', '南宫大锅菜']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '南宫湖'}), (f:Food {name: '南宫熏菜'})
               CREATE (a)-[:NEAR_FOOD {distance: '1.2km', tip: '湖边餐馆可品尝特色熏菜'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '南宫湖'}), (f:Food {name: '南宫大锅菜'})
               CREATE (a)-[:NEAR_FOOD {distance: '1km', tip: '景区周边小吃摊可体验传统美食'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '普彤寺'}), (f:Food {name: '南宫熏菜'})
               CREATE (a)-[:NEAR_FOOD {distance: '2.5km', tip: '市区餐馆有售特色熏菜'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '南宫湖'}), (ac:Accommodation {name: '南宫宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '2km'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '普彤寺'}), (ac:Accommodation {name: '南宫尚客优酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '3km'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '南宫'}), (t:Transportation)
               WHERE t.name IN ['南宫公交', '南宫汽车站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '南宫公交'}), (t2:Transportation {name: '南宫汽车站'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '公交直达客运站，方便前往邢台市区'}]->(t2)
           """)

        print("南宫旅游数据导入完成！")

    def import_shahe_data(self):
        """导入沙河旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (sh:City {name: '沙河', level: '县级市', description: '河北省县级市，邢台代管，中国玻璃城'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (beiwudangshan:Attraction {name: '北武当山', type: '自然景观', rating: 4.4, opening_hours: '7:30 - 17:00'}),
               (qinwanghu:Attraction {name: '秦王湖', type: '自然景观', rating: 4.3, opening_hours: '8:00 - 17:30'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (shahe_paigu:Food {name: '沙河排骨', type: '地方特色', price_range: '中', description: '肉质鲜嫩，香味浓郁'}),
               (shahe_guamian:Food {name: '沙河挂面', type: '传统美食', price_range: '低', description: '面条筋道，易于消化'}),
               (jinbaijia_hotel:Accommodation {name: '沙河金百家酒店', type: '三星级酒店', price_range: '中低', rating: 4.2}),
               (shahe_hotel:Accommodation {name: '沙河宾馆', type: '商务酒店', price_range: '中低', rating: 4.1}),
               (sh_bus:Transportation {name: '沙河公交', type: '公交', route: '覆盖市区', price: '1-2元'}),
               (sh_railway:Transportation {name: '沙河站', type: '火车站', route: '通往邢台等地', price: '根据里程'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '沙河'})
               WHERE a.name IN ['北武当山', '秦王湖']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '沙河'}), (f:Food)
               WHERE f.name IN ['沙河排骨', '沙河挂面']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '秦王湖'}), (f:Food {name: '沙河排骨'})
               CREATE (a)-[:NEAR_FOOD {distance: '1.5km', tip: '景区内餐馆可品尝特色排骨'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '秦王湖'}), (f:Food {name: '沙河挂面'})
               CREATE (a)-[:NEAR_FOOD {distance: '1km', tip: '湖边小吃店可体验传统挂面'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '北武当山'}), (f:Food {name: '沙河排骨'})
               CREATE (a)-[:NEAR_FOOD {distance: '6km', tip: '山脚下餐馆有特色排骨'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '北武当山'}), (ac:Accommodation {name: '沙河金百家酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '35km'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '秦王湖'}), (ac:Accommodation {name: '沙河宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '20km'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '沙河'}), (t:Transportation)
               WHERE t.name IN ['沙河公交', '沙河站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '沙河公交'}), (t2:Transportation {name: '沙河站'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '公交直达火车站，方便前往邢台市区'}]->(t2)
           """)

        print("沙河旅游数据导入完成！")

    def import_zhuozhou_data(self):
        """导入涿州旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (zz:City {name: '涿州', level: '县级市', description: '河北省县级市，保定代管，三国文化发祥地'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (sanyigong:Attraction {name: '三义宫', type: '人文景观', rating: 4.4, opening_hours: '8:30 - 17:00'}),
               (zhuozhou_filmstudio:Attraction {name: '涿州影视城', type: '人文景观', rating: 4.3, opening_hours: '9:00 - 17:00'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (zhuozhou_gongmi:Food {name: '涿州贡米', type: '地方特产', price_range: '中低', description: '米粒饱满，口感香糯'}),
               (zhangfei_jiu:Food {name: '张飞家酒', type: '地方特色', price_range: '中', description: '醇厚甘冽，回味悠长'}),
               (chengxin_building:Accommodation {name: '涿州诚信大厦', type: '四星级酒店', price_range: '中', rating: 4.3}),
               (huayilou_hotel:Accommodation {name: '涿州华谊楼酒店', type: '商务酒店', price_range: '中低', rating: 4.2}),
               (zz_bus:Transportation {name: '涿州公交', type: '公交', route: '覆盖市区', price: '1-2元'}),
               (zz_east_railway:Transportation {name: '涿州东站', type: '高铁站', route: '25分钟直达北京', price: '根据里程'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '涿州'})
               WHERE a.name IN ['三义宫', '涿州影视城']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '涿州'}), (f:Food)
               WHERE f.name IN ['涿州贡米', '张飞家酒']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '三义宫'}), (f:Food {name: '张飞家酒'})
               CREATE (a)-[:NEAR_FOOD {distance: '0.8km', tip: '景区内特产店可购买三国主题酒品'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '三义宫'}), (f:Food {name: '涿州贡米'})
               CREATE (a)-[:NEAR_FOOD {distance: '1km', tip: '景区周边商铺有售特色贡米'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '涿州影视城'}), (f:Food {name: '涿州贡米'})
               CREATE (a)-[:NEAR_FOOD {distance: '3km', tip: '影视城外餐馆可用贡米制作美食'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '三义宫'}), (ac:Accommodation {name: '涿州诚信大厦'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '5km'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '涿州影视城'}), (ac:Accommodation {name: '涿州华谊楼酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '2km'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '涿州'}), (t:Transportation)
               WHERE t.name IN ['涿州公交', '涿州东站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '涿州公交'}), (t2:Transportation {name: '涿州东站'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '公交专线直达高铁站，25分钟快速通达北京'}]->(t2)
           """)

        print("涿州旅游数据导入完成！")

    def import_dingzhou_data(self):
        """导入定州旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (dz:City {name: '定州', level: '县级市', description: '河北省县级市，省直管市，中山古都'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (kaiyuansi_tower:Attraction {name: '定州开元寺塔', type: '人文景观', rating: 4.5, opening_hours: '8:30 - 17:00'}),
               (dingzhou_gongyuan:Attraction {name: '定州贡院', type: '人文景观', rating: 4.4, opening_hours: '9:00 - 16:30'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (dingzhou_menzi:Food {name: '定州焖子', type: '地方特色', price_range: '中低', description: '口感细腻，香味浓郁'}),
               (dingzhou_shoubaichang:Food {name: '定州手掰肠', type: '传统美食', price_range: '中低', description: '肉质紧实，风味独特'}),
               (dingzhou_international:Accommodation {name: '定州国际酒店', type: '四星级酒店', price_range: '中', rating: 4.4}),
               (zhongshan_hotel:Accommodation {name: '定州中山宾馆', type: '商务酒店', price_range: '中低', rating: 4.2}),
               (dz_bus:Transportation {name: '定州公交', type: '公交', route: '覆盖市区', price: '1-2元'}),
               (dz_east_railway:Transportation {name: '定州东站', type: '高铁站', route: '通往石家庄等地', price: '根据里程'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '定州'})
               WHERE a.name IN ['定州开元寺塔', '定州贡院']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '定州'}), (f:Food)
               WHERE f.name IN ['定州焖子', '定州手掰肠']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '定州贡院'}), (f:Food {name: '定州焖子'})
               CREATE (a)-[:NEAR_FOOD {distance: '0.6km', tip: '贡院周边餐馆可品尝特色焖子'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '定州贡院'}), (f:Food {name: '定州手掰肠'})
               CREATE (a)-[:NEAR_FOOD {distance: '0.8km', tip: '景区附近老字号店铺有售'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '定州开元寺塔'}), (f:Food {name: '定州手掰肠'})
               CREATE (a)-[:NEAR_FOOD {distance: '1.2km', tip: '古塔周边小吃街可体验'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '定州开元寺塔'}), (ac:Accommodation {name: '定州国际酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '2km'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '定州贡院'}), (ac:Accommodation {name: '定州中山宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '1.5km', tip: '毗邻历史文化街区，出行便利'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '定州'}), (t:Transportation)
               WHERE t.name IN ['定州公交', '定州东站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '定州公交'}), (t2:Transportation {name: '定州东站'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '公交直达高铁站，方便前往石家庄、北京'}]->(t2)
           """)

        print("定州旅游数据导入完成！")

    def import_anguo_data(self):
        """导入安国旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (ag:City {name: '安国', level: '县级市', description: '河北省县级市，保定代管，中国药都'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (yaowangmiao:Attraction {name: '药王庙', type: '人文景观', rating: 4.5, opening_hours: '8:30 - 17:00'}),
               (dongfang_yaocheng:Attraction {name: '东方药城', type: '商业旅游', rating: 4.4, opening_hours: '9:00 - 17:00'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (anguo_yaoshan:Food {name: '安国药膳', type: '地方特色', price_range: '中', description: '药食同源，养生保健'}),
               (qizhou_jiu:Food {name: '祁州酒', type: '地方特产', price_range: '中低', description: '酒香浓郁，口感醇厚'}),
               (yaodu_hotel:Accommodation {name: '安国药都大酒店', type: '四星级酒店', price_range: '中', rating: 4.4}),
               (qizhou_hotel:Accommodation {name: '安国祁州宾馆', type: '商务酒店', price_range: '中低', rating: 4.2}),
               (ag_bus:Transportation {name: '安国公交', type: '公交', route: '覆盖市区', price: '1-2元'}),
               (ag_bus_station:Transportation {name: '安国汽车站', type: '客运站', route: '通往保定等地', price: '根据里程'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '安国'})
               WHERE a.name IN ['药王庙', '东方药城']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '安国'}), (f:Food)
               WHERE f.name IN ['安国药膳', '祁州酒']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '东方药城'}), (f:Food {name: '安国药膳'})
               CREATE (a)-[:NEAR_FOOD {distance: '0.5km', tip: '药城周边餐馆可品尝养生药膳'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '药王庙'}), (f:Food {name: '祁州酒'})
               CREATE (a)-[:NEAR_FOOD {distance: '0.8km', tip: '景区特产店有售传统药酒'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '东方药城'}), (f:Food {name: '祁州酒'})
               CREATE (a)-[:NEAR_FOOD {distance: '1km', tip: '药城周边商铺可购买'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '药王庙'}), (ac:Accommodation {name: '安国药都大酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '1.2km', tip: '毗邻药材市场，药文化主题突出'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '东方药城'}), (ac:Accommodation {name: '安国祁州宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '0.7km'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '安国'}), (t:Transportation)
               WHERE t.name IN ['安国公交', '安国汽车站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '安国公交'}), (t2:Transportation {name: '安国汽车站'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '公交直达客运站，方便前往保定市区'}]->(t2)
           """)

        print("安国旅游数据导入完成！")

    def import_gaobeidian_data(self):
        """导入高碑店旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (gbd:City {name: '高碑店', level: '县级市', description: '河北省县级市，保定代管，京津冀重要节点城市'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (world_doors_windows:Attraction {name: '世界门窗小镇', type: '工业旅游', rating: 4.3, opening_hours: '9:00 - 16:30'}),
               (ziquanhe:Attraction {name: '紫泉河景区', type: '自然景观', rating: 4.2, opening_hours: '8:00 - 17:00'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (gaobeidian_doufus:Food {name: '高碑店豆腐丝', type: '地方特产', price_range: '低', description: '口感细腻，豆香浓郁'}),
               (huangtao_canned:Food {name: '黄桃罐头', type: '地方特色', price_range: '低', description: '果肉饱满，甜度适中'}),
               (pengda_hotel:Accommodation {name: '高碑店鹏达国际酒店', type: '四星级酒店', price_range: '中', rating: 4.3}),
               (yankang_hotel:Accommodation {name: '高碑店燕康宾馆', type: '商务酒店', price_range: '中低', rating: 4.1}),
               (gbd_bus:Transportation {name: '高碑店公交', type: '公交', route: '覆盖市区', price: '1-2元'}),
               (gbd_east_railway:Transportation {name: '高碑店东站', type: '高铁站', route: '30分钟直达北京', price: '根据里程'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '高碑店'})
               WHERE a.name IN ['世界门窗小镇', '紫泉河景区']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '高碑店'}), (f:Food)
               WHERE f.name IN ['高碑店豆腐丝', '黄桃罐头']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '世界门窗小镇'}), (f:Food {name: '高碑店豆腐丝'})
               CREATE (a)-[:NEAR_FOOD {distance: '1.2km', tip: '小镇配套商业区有售特色豆腐丝'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '世界门窗小镇'}), (f:Food {name: '黄桃罐头'})
               CREATE (a)-[:NEAR_FOOD {distance: '1km', tip: '景区出口特产店可购买'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '紫泉河景区'}), (f:Food {name: '高碑店豆腐丝'})
               CREATE (a)-[:NEAR_FOOD {distance: '3km', tip: '景区周边餐馆可品尝'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '世界门窗小镇'}), (ac:Accommodation {name: '高碑店鹏达国际酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '5km'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '紫泉河景区'}), (ac:Accommodation {name: '高碑店燕康宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '2.5km'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '高碑店'}), (t:Transportation)
               WHERE t.name IN ['高碑店公交', '高碑店东站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '高碑店公交'}), (t2:Transportation {name: '高碑店东站'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '公交专线直达高铁站，30分钟快速通达北京'}]->(t2)
           """)

        print("高碑店旅游数据导入完成！")

    def import_pingquan_data(self):
        """导入平泉旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (pq:City {name: '平泉', level: '县级市', description: '河北省县级市，承德代管，契丹文化发祥地'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (liaoheyuan:Attraction {name: '辽河源国家森林公园', type: '自然景观', rating: 4.6, opening_hours: '8:00 - 17:30'}),
               (zezhouyuan:Attraction {name: '泽州园', type: '人文景观', rating: 4.4, opening_hours: '8:30 - 17:00'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (pingquan_yangtang:Food {name: '平泉羊汤', type: '地方特色', price_range: '中低', description: '汤鲜味美，营养丰富'}),
               (gaidao_rou:Food {name: '改刀肉', type: '传统美食', price_range: '中', description: '刀工精细，口感独特'}),
               (jinshiji_hotel:Accommodation {name: '平泉金世纪酒店', type: '三星级酒店', price_range: '中低', rating: 4.3}),
               (shanzhuang_hotel:Accommodation {name: '平泉山庄宾馆', type: '商务酒店', price_range: '中低', rating: 4.2}),
               (pq_bus:Transportation {name: '平泉公交', type: '公交', route: '覆盖市区', price: '1-2元'}),
               (pq_north_railway:Transportation {name: '平泉北站', type: '高铁站', route: '通往承德等地', price: '根据里程'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '平泉'})
               WHERE a.name IN ['辽河源国家森林公园', '泽州园']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '平泉'}), (f:Food)
               WHERE f.name IN ['平泉羊汤', '改刀肉']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '泽州园'}), (f:Food {name: '平泉羊汤'})
               CREATE (a)-[:NEAR_FOOD {distance: '0.8km', tip: '园区周边餐馆可品尝特色羊汤'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '泽州园'}), (f:Food {name: '改刀肉'})
               CREATE (a)-[:NEAR_FOOD {distance: '1km', tip: '景区附近老字号可体验传统改刀肉'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '辽河源国家森林公园'}), (f:Food {name: '平泉羊汤'})
               CREATE (a)-[:NEAR_FOOD {distance: '15km', tip: '返回市区途中可品尝正宗羊汤'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '辽河源国家森林公园'}), (ac:Accommodation {name: '平泉金世纪酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '40km'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '泽州园'}), (ac:Accommodation {name: '平泉山庄宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '1.2km', tip: '毗邻契丹文化景区，出行便利'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '平泉'}), (t:Transportation)
               WHERE t.name IN ['平泉公交', '平泉北站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '平泉公交'}), (t2:Transportation {name: '平泉北站'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '公交直达高铁站，方便前往承德市区'}]->(t2)
           """)

        print("平泉旅游数据导入完成！")

    def import_botou_data(self):
        """导入泊头旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (bt:City {name: '泊头', level: '县级市', description: '河北省县级市，沧州代管，中国铸造之乡，鸭梨之乡'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (botou_qingzhensi:Attraction {name: '泊头清真寺', type: '人文景观', rating: 4.4, opening_hours: '8:30 - 17:00'}),
               (sanjing_dayunhe:Attraction {name: '三井大运河遗址', type: '人文景观', rating: 4.3, opening_hours: '全天开放'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (botou_yali:Food {name: '泊头鸭梨', type: '地方特产', price_range: '低', description: '汁多味甜，肉质细腻'}),
               (jiaohe_jianbing:Food {name: '交河煎饼', type: '传统小吃', price_range: '低', description: '薄如蝉翼，口感酥脆'}),
               (zhuorui_hotel:Accommodation {name: '泊头卓锐酒店', type: '三星级酒店', price_range: '中低', rating: 4.3}),
               (botou_hotel:Accommodation {name: '泊头宾馆', type: '商务酒店', price_range: '中低', rating: 4.1}),
               (bt_bus:Transportation {name: '泊头公交', type: '公交', route: '覆盖市区', price: '1-2元'}),
               (bt_railway:Transportation {name: '泊头站', type: '火车站', route: '通往沧州等地', price: '根据里程'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '泊头'})
               WHERE a.name IN ['泊头清真寺', '三井大运河遗址']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '泊头'}), (f:Food)
               WHERE f.name IN ['泊头鸭梨', '交河煎饼']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '三井大运河遗址'}), (f:Food {name: '交河煎饼'})
               CREATE (a)-[:NEAR_FOOD {distance: '0.6km', tip: '遗址周边小吃摊可品尝传统煎饼'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '三井大运河遗址'}), (f:Food {name: '泊头鸭梨'})
               CREATE (a)-[:NEAR_FOOD {distance: '1km', tip: '运河边特产店有售新鲜鸭梨'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '泊头清真寺'}), (f:Food {name: '交河煎饼'})
               CREATE (a)-[:NEAR_FOOD {distance: '2km', tip: '市区老字号摊位可体验特色小吃'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '泊头清真寺'}), (ac:Accommodation {name: '泊头卓锐酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '3km'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '三井大运河遗址'}), (ac:Accommodation {name: '泊头宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '1.5km', tip: '毗邻运河遗址，历史氛围浓厚'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '泊头'}), (t:Transportation)
               WHERE t.name IN ['泊头公交', '泊头站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '泊头公交'}), (t2:Transportation {name: '泊头站'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '公交直达火车站，方便前往沧州等地'}]->(t2)
           """)

        print("泊头旅游数据导入完成！")

    def import_renqiu_data(self):
        """导入任丘旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (rq:City {name: '任丘', level: '县级市', description: '河北省县级市，沧州代管，华北油田总部所在地'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (baiyangdian:Attraction {name: '白洋淀', type: '自然景观', rating: 4.6, opening_hours: '8:00 - 18:00'}),
               (maozhoumiao:Attraction {name: '鄚州庙', type: '人文景观', rating: 4.3, opening_hours: '8:30 - 17:00'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (baiyangdian_fishbanquet:Food {name: '白洋淀全鱼宴', type: '地方特色', price_range: '中高', description: '食材新鲜，烹饪讲究'}),
               (renqiu_laodoufu:Food {name: '任丘老豆腐', type: '传统小吃', price_range: '低', description: '口感细腻，豆香浓郁'}),
               (huayou_hotel:Accommodation {name: '任丘华油宾馆', type: '四星级酒店', price_range: '中', rating: 4.4}),
               (renqiu_international:Accommodation {name: '任丘国际酒店', type: '商务酒店', price_range: '中', rating: 4.3}),
               (rq_bus:Transportation {name: '任丘公交', type: '公交', route: '覆盖市区', price: '1-2元'}),
               (rq_west_railway:Transportation {name: '任丘西站', type: '高铁站', route: '通往雄安等地', price: '根据里程'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '任丘'})
               WHERE a.name IN ['白洋淀', '鄚州庙']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '任丘'}), (f:Food)
               WHERE f.name IN ['白洋淀全鱼宴', '任丘老豆腐']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '白洋淀'}), (f:Food {name: '白洋淀全鱼宴'})
               CREATE (a)-[:NEAR_FOOD {distance: '0.5km', tip: '淀边渔村餐馆可品尝新鲜全鱼宴'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '白洋淀'}), (f:Food {name: '任丘老豆腐'})
               CREATE (a)-[:NEAR_FOOD {distance: '5km', tip: '返回市区途中可体验传统小吃'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '鄚州庙'}), (f:Food {name: '任丘老豆腐'})
               CREATE (a)-[:NEAR_FOOD {distance: '2km', tip: '景区周边早餐店可品尝'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '白洋淀'}), (ac:Accommodation {name: '任丘华油宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '15km'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '鄚州庙'}), (ac:Accommodation {name: '任丘国际酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '8km'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '任丘'}), (t:Transportation)
               WHERE t.name IN ['任丘公交', '任丘西站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '任丘公交'}), (t2:Transportation {name: '任丘西站'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '公交直达高铁站，方便前往雄安新区'}]->(t2)
           """)

        print("任丘旅游数据导入完成！")

    def import_huanghua_data(self):
        """导入黄骅旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (hh:City {name: '黄骅', level: '县级市', description: '河北省县级市，沧州代管，渤海湾重要港口城市'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (huanghua_port:Attraction {name: '黄骅港', type: '工业旅游', rating: 4.4, opening_hours: '9:00 - 16:30'}),
               (nandagang_wetland:Attraction {name: '南大港湿地', type: '自然景观', rating: 4.5, opening_hours: '8:00 - 17:30'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (huanghua_seafood:Food {name: '黄骅海鲜', type: '地方特色', price_range: '中高', description: '新鲜美味，品种丰富'}),
               (huanghua_dongzao:Food {name: '黄骅冬枣', type: '地方特产', price_range: '中低', description: '脆甜可口，营养丰富'}),
               (xinyuan_hotel:Accommodation {name: '黄骅信源酒店', type: '四星级酒店', price_range: '中', rating: 4.4}),
               (jindu_garden:Accommodation {name: '黄骅金都花园酒店', type: '商务酒店', price_range: '中', rating: 4.3}),
               (hh_bus:Transportation {name: '黄骅公交', type: '公交', route: '覆盖市区', price: '1-2元'}),
               (hh_railway:Transportation {name: '黄骅站', type: '火车站', route: '通往沧州等地', price: '根据里程'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '黄骅'})
               WHERE a.name IN ['黄骅港', '南大港湿地']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '黄骅'}), (f:Food)
               WHERE f.name IN ['黄骅海鲜', '黄骅冬枣']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '黄骅港'}), (f:Food {name: '黄骅海鲜'})
               CREATE (a)-[:NEAR_FOOD {distance: '0.8km', tip: '港口周边渔家乐可品尝现捕海鲜'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '黄骅港'}), (f:Food {name: '黄骅冬枣'})
               CREATE (a)-[:NEAR_FOOD {distance: '5km', tip: '港区特产店有售新鲜冬枣'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '南大港湿地'}), (f:Food {name: '黄骅海鲜'})
               CREATE (a)-[:NEAR_FOOD {distance: '12km', tip: '返回市区途中可品尝海鲜大餐'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '黄骅港'}), (ac:Accommodation {name: '黄骅信源酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '8km'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '南大港湿地'}), (ac:Accommodation {name: '黄骅金都花园酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '20km'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '黄骅'}), (t:Transportation)
               WHERE t.name IN ['黄骅公交', '黄骅站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '黄骅公交'}), (t2:Transportation {name: '黄骅站'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '公交直达火车站，方便前往沧州、天津等地'}]->(t2)
           """)

        print("黄骅旅游数据导入完成！")

    def import_hebei_data(self):
        """导入河间旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (hj:City {name: '河间', level: '县级市', description: '河北省县级市，沧州代管，中国驴肉火烧之乡'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (hebei_fu署:Attraction {name: '河间府署', type: '人文景观', rating: 4.4, opening_hours: '8:30 - 17:00'}),
               (guangming_xiyuan:Attraction {name: '光明戏院', type: '人文景观', rating: 4.3, opening_hours: '9:00 - 17:00'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (hebei_lvrouhuoshao:Food {name: '河间驴肉火烧', type: '地方特色', price_range: '中低', description: '外酥里嫩，肉香四溢'}),
               (hebei_xunrou:Food {name: '河间熏肉', type: '传统美食', price_range: '中低', description: '色泽红亮，风味独特'}),
               (huayuan_hotel:Accommodation {name: '河间华苑宾馆', type: '四星级酒店', price_range: '中', rating: 4.3}),
               (guoxin_hotel:Accommodation {name: '河间国欣宾馆', type: '商务酒店', price_range: '中低', rating: 4.2}),
               (hj_bus:Transportation {name: '河间公交', type: '公交', route: '覆盖市区', price: '1-2元'}),
               (hj_bus_station:Transportation {name: '河间汽车站', type: '客运站', route: '通往沧州等地', price: '根据里程'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '河间'})
               WHERE a.name IN ['河间府署', '光明戏院']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '河间'}), (f:Food)
               WHERE f.name IN ['河间驴肉火烧', '河间熏肉']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '河间府署'}), (f:Food {name: '河间驴肉火烧'})
               CREATE (a)-[:NEAR_FOOD {distance: '0.5km', tip: '府署周边老字号可品尝正宗火烧'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '河间府署'}), (f:Food {name: '河间熏肉'})
               CREATE (a)-[:NEAR_FOOD {distance: '0.7km', tip: '景区附近商铺有售传统熏肉'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '光明戏院'}), (f:Food {name: '河间驴肉火烧'})
               CREATE (a)-[:NEAR_FOOD {distance: '1.2km', tip: '戏院周边小吃街可体验特色美食'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '河间府署'}), (ac:Accommodation {name: '河间华苑宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '2km'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '光明戏院'}), (ac:Accommodation {name: '河间国欣宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '1.5km', tip: '毗邻文化街区，出行便利'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '河间'}), (t:Transportation)
               WHERE t.name IN ['河间公交', '河间汽车站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '河间公交'}), (t2:Transportation {name: '河间汽车站'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '公交直达客运站，方便前往沧州、保定等地'}]->(t2)
           """)

        print("河间旅游数据导入完成！")

    def import_bazhou_data(self):
        """导入霸州旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (bz:City {name: '霸州', level: '县级市', description: '河北省县级市，廊坊代管，京津冀协同发展重要节点'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (longquan_chansi:Attraction {name: '霸州龙泉禅寺', type: '人文景观', rating: 4.4, opening_hours: '8:00 - 17:00'}),
               (zhonghua_xiqucheng:Attraction {name: '中华戏曲城', type: '人文景观', rating: 4.3, opening_hours: '9:00 - 17:00'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (bazhou_sumao:Food {name: '霸州素冒汤', type: '地方特色', price_range: '低', description: '汤鲜味美，配料丰富'}),
               (shengfang_songhua:Food {name: '胜芳松花蛋', type: '传统美食', price_range: '中低', description: '蛋清透明，蛋黄绵软'}),
               (meigui_zhuangyuan:Accommodation {name: '霸州玫瑰庄园温泉酒店', type: '四星级酒店', price_range: '中', rating: 4.4}),
               (yijia_hotel:Accommodation {name: '霸州驿家酒店', type: '商务酒店', price_range: '中低', rating: 4.2}),
               (bz_bus:Transportation {name: '霸州公交', type: '公交', route: '覆盖市区', price: '1-2元'}),
               (bz_west_railway:Transportation {name: '霸州西站', type: '高铁站', route: '25分钟直达北京', price: '根据里程'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '霸州'})
               WHERE a.name IN ['霸州龙泉禅寺', '中华戏曲城']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '霸州'}), (f:Food)
               WHERE f.name IN ['霸州素冒汤', '胜芳松花蛋']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '中华戏曲城'}), (f:Food {name: '霸州素冒汤'})
               CREATE (a)-[:NEAR_FOOD {distance: '0.8km', tip: '戏曲城周边餐馆可品尝特色素汤'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '中华戏曲城'}), (f:Food {name: '胜芳松花蛋'})
               CREATE (a)-[:NEAR_FOOD {distance: '1km', tip: '景区特产店有售传统松花蛋'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '霸州龙泉禅寺'}), (f:Food {name: '霸州素冒汤'})
               CREATE (a)-[:NEAR_FOOD {distance: '1.5km', tip: '寺院周边素菜馆可体验特色汤品'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '霸州龙泉禅寺'}), (ac:Accommodation {name: '霸州玫瑰庄园温泉酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '3km'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '中华戏曲城'}), (ac:Accommodation {name: '霸州驿家酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '2km', tip: '毗邻戏曲文化景区，出行便利'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '霸州'}), (t:Transportation)
               WHERE t.name IN ['霸州公交', '霸州西站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '霸州公交'}), (t2:Transportation {name: '霸州西站'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '公交专线直达高铁站，25分钟快速通达北京'}]->(t2)
           """)

        print("霸州旅游数据导入完成！")

    def import_sanhe_data(self):
        """导入三河旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (sh:City {name: '三河', level: '县级市', description: '河北省县级市，廊坊代管，毗邻北京通州区'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (yanjiao_arboretum:Attraction {name: '燕郊植物园', type: '自然景观', rating: 4.3, opening_hours: '8:00 - 17:30'}),
               (sanhe_canyon:Attraction {name: '三河大峡谷', type: '自然景观', rating: 4.2, opening_hours: '8:30 - 17:00'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (sanhe_dousi:Food {name: '三河豆丝', type: '地方特产', price_range: '低', description: '豆香浓郁，口感细腻'}),
               (yanjiao_roastduck:Food {name: '燕郊烤鸭', type: '地方特色', price_range: '中', description: '皮脆肉嫩，风味独特'}),
               (fucheng_hotel:Accommodation {name: '三河福成国际酒店', type: '四星级酒店', price_range: '中', rating: 4.4}),
               (yanlong_hotel:Accommodation {name: '三河燕龙酒店', type: '商务酒店', price_range: '中低', rating: 4.2}),
               (sh_bus:Transportation {name: '三河公交', type: '公交', route: '覆盖市区', price: '1-2元'}),
               (yanjiao_railway:Transportation {name: '燕郊站', type: '火车站', route: '30分钟直达北京', price: '根据里程'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '三河'})
               WHERE a.name IN ['燕郊植物园', '三河大峡谷']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '三河'}), (f:Food)
               WHERE f.name IN ['三河豆丝', '燕郊烤鸭']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '燕郊植物园'}), (f:Food {name: '燕郊烤鸭'})
               CREATE (a)-[:NEAR_FOOD {distance: '1.2km', tip: '植物园周边餐馆可品尝特色烤鸭'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '燕郊植物园'}), (f:Food {name: '三河豆丝'})
               CREATE (a)-[:NEAR_FOOD {distance: '1km', tip: '景区出口特产店有售豆丝'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '三河大峡谷'}), (f:Food {name: '三河豆丝'})
               CREATE (a)-[:NEAR_FOOD {distance: '8km', tip: '返回市区途中可购买特色豆丝'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '燕郊植物园'}), (ac:Accommodation {name: '三河福成国际酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '3km'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '三河大峡谷'}), (ac:Accommodation {name: '三河燕龙酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '10km', tip: '靠近峡谷景区，适合休闲住宿'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '三河'}), (t:Transportation)
               WHERE t.name IN ['三河公交', '燕郊站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '三河公交'}), (t2:Transportation {name: '燕郊站'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '公交直达火车站，30分钟快速通达北京通州'}]->(t2)
           """)

        print("三河旅游数据导入完成！")

    def import_shenzhou_data(self):
        """导入深州旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (sz:City {name: '深州', level: '县级市', description: '河北省县级市，衡水代管，蜜桃之乡'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (shenzhou_peach_garden:Attraction {name: '深州蜜桃观光园', type: '农业观光', rating: 4.4, opening_hours: '8:00 - 17:30'}),
               (yingyi_yicang:Attraction {name: '盈亿义仓', type: '人文景观', rating: 4.2, opening_hours: '8:30 - 17:00'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (shenzhou_peach:Food {name: '深州蜜桃', type: '地方特产', price_range: '中低', description: '汁多味甜，肉质细腻'}),
               (shenzhou_sutang:Food {name: '深州酥糖', type: '传统糕点', price_range: '低', description: '香甜酥脆，入口即化'}),
               (taishan_road_hotel:Accommodation {name: '深州泰山东路宾馆', type: '三星级酒店', price_range: '中低', rating: 4.3}),
               (yijia365_hotel:Accommodation {name: '深州驿家365酒店', type: '商务酒店', price_range: '中低', rating: 4.1}),
               (sz_bus:Transportation {name: '深州公交', type: '公交', route: '覆盖市区', price: '1-2元'}),
               (sz_railway:Transportation {name: '深州站', type: '火车站', route: '通往衡水等地', price: '根据里程'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '深州'})
               WHERE a.name IN ['深州蜜桃观光园', '盈亿义仓']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '深州'}), (f:Food)
               WHERE f.name IN ['深州蜜桃', '深州酥糖']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '深州蜜桃观光园'}), (f:Food {name: '深州蜜桃'})
               CREATE (a)-[:NEAR_FOOD {distance: '0.3km', tip: '观光园内可采摘品尝新鲜蜜桃'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '深州蜜桃观光园'}), (f:Food {name: '深州酥糖'})
               CREATE (a)-[:NEAR_FOOD {distance: '2km', tip: '园区出口特产店有售蜜桃味酥糖'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '盈亿义仓'}), (f:Food {name: '深州酥糖'})
               CREATE (a)-[:NEAR_FOOD {distance: '1km', tip: '义仓周边老字号店铺可购买传统酥糖'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '深州蜜桃观光园'}), (ac:Accommodation {name: '深州泰山东路宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '5km', tip: '靠近蜜桃产区，方便采摘体验'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '盈亿义仓'}), (ac:Accommodation {name: '深州驿家365酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '1.5km'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '深州'}), (t:Transportation)
               WHERE t.name IN ['深州公交', '深州站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '深州公交'}), (t2:Transportation {name: '深州站'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '公交直达火车站，方便前往衡水市区'}]->(t2)
           """)

        print("深州旅游数据导入完成！")

    def import_taiyuan_data(self):
        """导入太原旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (ty:City {name: '太原', level: '地级市', description: '山西省省会，国家历史文化名城，能源重化工基地'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (jinci:Attraction {name: '晋祠', type: '人文景观', rating: 4.7, opening_hours: '8:30 - 17:30'}),
               (tianlongshan:Attraction {name: '天龙山石窟', type: '人文景观', rating: 4.6, opening_hours: '8:30 - 17:00'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (daoxiaomian:Food {name: '刀削面', type: '山西面食', price_range: '低', description: '面条筋道，卤汁鲜美'}),
               (guoyourou:Food {name: '过油肉', type: '山西菜', price_range: '中低', description: '肉质滑嫩，醋香浓郁'}),
               (wanda_culture:Accommodation {name: '太原万达文华酒店', type: '五星级酒店', price_range: '高', rating: 4.7}),
               (kempinski:Accommodation {name: '太原凯宾斯基饭店', type: '五星级酒店', price_range: '高', rating: 4.6}),
               (ty_metro2:Transportation {name: '太原地铁2号线', type: '地铁', route: '尖草坪-西桥', price: '2-6元'}),
               (wusu_bus:Transportation {name: '武宿国际机场大巴', type: '机场巴士', route: '市区-机场', price: '15-25元'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '太原'})
               WHERE a.name IN ['晋祠', '天龙山石窟']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '太原'}), (f:Food)
               WHERE f.name IN ['刀削面', '过油肉']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '晋祠'}), (f:Food {name: '刀削面'})
               CREATE (a)-[:NEAR_FOOD {distance: '20km', tip: '返回市区后推荐品尝老字号刀削面'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '晋祠'}), (f:Food {name: '过油肉'})
               CREATE (a)-[:NEAR_FOOD {distance: '18km', tip: '市区晋菜餐馆可体验传统过油肉'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '天龙山石窟'}), (f:Food {name: '刀削面'})
               CREATE (a)-[:NEAR_FOOD {distance: '30km', tip: '下山后前往市区品尝地道面食'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '晋祠'}), (ac:Accommodation {name: '太原万达文华酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '25km', tip: '位于市中心，方便游览后休整'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '天龙山石窟'}), (ac:Accommodation {name: '太原凯宾斯基饭店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '35km'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '太原'}), (t:Transportation)
               WHERE t.name IN ['太原地铁2号线', '武宿国际机场大巴']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '太原地铁2号线'}), (t2:Transportation {name: '武宿国际机场大巴'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '地铁2号线大南门站可换乘机场大巴，直达武宿机场'}]->(t2)
           """)

        print("太原旅游数据导入完成！")

    def import_datong_data(self):
        """导入大同旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (dt:City {name: '大同', level: '地级市', description: '中国九大古都之一，国家历史文化名城，煤都'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (yungang_grottoes:Attraction {name: '云冈石窟', type: '人文景观', rating: 4.8, opening_hours: '9:00 - 17:00'}),
               (hanging_monastery:Attraction {name: '悬空寺', type: '人文景观', rating: 4.7, opening_hours: '8:00 - 17:30'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (datong_daoxiaomian:Food {name: '大同刀削面', type: '山西面食', price_range: '低', description: '面条筋道，卤汁香浓'}),
               (yangzage:Food {name: '羊杂割', type: '地方小吃', price_range: '中低', description: '汤鲜味美，暖胃驱寒'}),
               (wangfu_hotel:Accommodation {name: '大同王府至尊酒店', type: '五星级酒店', price_range: '高', rating: 4.6}),
               (yungang_international:Accommodation {name: '大同云冈国际酒店', type: '五星级酒店', price_range: '高', rating: 4.5}),
               (dt_bus:Transportation {name: '大同公交', type: '公交', route: '覆盖市区景点', price: '1-2元'}),
               (yungang_tour_bus:Transportation {name: '云冈区旅游专线', type: '旅游巴士', route: '市区-云冈石窟', price: '5元'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '大同'})
               WHERE a.name IN ['云冈石窟', '悬空寺']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '大同'}), (f:Food)
               WHERE f.name IN ['大同刀削面', '羊杂割']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '云冈石窟'}), (f:Food {name: '大同刀削面'})
               CREATE (a)-[:NEAR_FOOD {distance: '15km', tip: '返回市区途中可品尝老字号刀削面'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '云冈石窟'}), (f:Food {name: '羊杂割'})
               CREATE (a)-[:NEAR_FOOD {distance: '14km', tip: '景区周边餐馆可体验特色羊杂'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '悬空寺'}), (f:Food {name: '大同刀削面'})
               CREATE (a)-[:NEAR_FOOD {distance: '60km', tip: '返回大同市区后推荐品尝地道面食'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '云冈石窟'}), (ac:Accommodation {name: '大同云冈国际酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '12km', tip: '靠近云冈石窟，方便文化游览'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '悬空寺'}), (ac:Accommodation {name: '大同王府至尊酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '65km'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '大同'}), (t:Transportation)
               WHERE t.name IN ['大同公交', '云冈区旅游专线']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '大同公交'}), (t2:Transportation {name: '云冈区旅游专线'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '市区公交枢纽可换乘旅游专线直达云冈石窟'}]->(t2)
           """)

        print("大同旅游数据导入完成！")

    def import_yangquan_data(self):
        """导入阳泉旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (yq:City {name: '阳泉', level: '地级市', description: '山西省地级市，中共创建第一城，煤炭工业城市'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (niangziguan:Attraction {name: '娘子关', type: '人文景观', rating: 4.5, opening_hours: '8:00 - 18:00'}),
               (cuifengshan:Attraction {name: '翠枫山', type: '自然景观', rating: 4.3, opening_hours: '8:30 - 17:30'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (yangquan_guoyourou:Food {name: '阳泉过油肉', type: '地方特色', price_range: '中低', description: '肉质滑嫩，醋香浓郁'}),
               (pingding_huangguagan:Food {name: '平定黄瓜干', type: '地方特产', price_range: '低', description: '口感独特，便于保存'}),
               (yangquan_hotel:Accommodation {name: '阳泉宾馆', type: '四星级酒店', price_range: '中', rating: 4.4}),
               (beiguomingzhu_hotel:Accommodation {name: '阳泉北国明珠酒店', type: '商务酒店', price_range: '中', rating: 4.3}),
               (yq_bus:Transportation {name: '阳泉公交', type: '公交', route: '覆盖市区', price: '1-2元'}),
               (yq_north_railway:Transportation {name: '阳泉北站', type: '高铁站', route: '通往太原等地', price: '根据里程'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '阳泉'})
               WHERE a.name IN ['娘子关', '翠枫山']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '阳泉'}), (f:Food)
               WHERE f.name IN ['阳泉过油肉', '平定黄瓜干']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '娘子关'}), (f:Food {name: '阳泉过油肉'})
               CREATE (a)-[:NEAR_FOOD {distance: '2km', tip: '关城周边餐馆可品尝特色过油肉'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '娘子关'}), (f:Food {name: '平定黄瓜干'})
               CREATE (a)-[:NEAR_FOOD {distance: '5km', tip: '景区特产店有售传统黄瓜干'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '翠枫山'}), (f:Food {name: '阳泉过油肉'})
               CREATE (a)-[:NEAR_FOOD {distance: '18km', tip: '返回市区后可体验正宗过油肉'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '娘子关'}), (ac:Accommodation {name: '阳泉宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '40km'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '翠枫山'}), (ac:Accommodation {name: '阳泉北国明珠酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '15km', tip: '靠近自然景区，适合休闲住宿'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '阳泉'}), (t:Transportation)
               WHERE t.name IN ['阳泉公交', '阳泉北站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '阳泉公交'}), (t2:Transportation {name: '阳泉北站'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '公交直达高铁站，方便前往太原、石家庄等地'}]->(t2)
           """)

        print("阳泉旅游数据导入完成！")

    def import_changzhi_data(self):
        """导入长治旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (cz:City {name: '长治', level: '地级市', description: '山西省地级市，国家园林城市，太行明珠'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (taihang_canyon:Attraction {name: '太行山大峡谷', type: '自然景观', rating: 4.7, opening_hours: '8:00 - 17:30'}),
               (laodingshan:Attraction {name: '老顶山国家森林公园', type: '自然景观', rating: 4.5, opening_hours: '8:30 - 17:00'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (changzhi_lalvrou:Food {name: '长治腊驴肉', type: '地方特产', price_range: '中', description: '肉质紧实，香味浓郁'}),
               (shangdang_huzhouzi:Food {name: '上党糊肘子', type: '传统美食', price_range: '中低', description: '软烂入味，肥而不腻'}),
               (yidong_international:Accommodation {name: '长治益东国际酒店', type: '五星级酒店', price_range: '高', rating: 4.6}),
               (changzhi_hotel:Accommodation {name: '长治宾馆', type: '四星级酒店', price_range: '中', rating: 4.4}),
               (cz_bus:Transportation {name: '长治公交', type: '公交', route: '覆盖市区', price: '1-2元'}),
               (cz_east_railway:Transportation {name: '长治东站', type: '高铁站', route: '通往太原等地', price: '根据里程'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '长治'})
               WHERE a.name IN ['太行山大峡谷', '老顶山国家森林公园']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '长治'}), (f:Food)
               WHERE f.name IN ['长治腊驴肉', '上党糊肘子']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '老顶山国家森林公园'}), (f:Food {name: '长治腊驴肉'})
               CREATE (a)-[:NEAR_FOOD {distance: '5km', tip: '下山后市区餐馆可品尝腊驴肉'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '老顶山国家森林公园'}), (f:Food {name: '上党糊肘子'})
               CREATE (a)-[:NEAR_FOOD {distance: '4km', tip: '景区周边老字号可体验传统糊肘子'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '太行山大峡谷'}), (f:Food {name: '长治腊驴肉'})
               CREATE (a)-[:NEAR_FOOD {distance: '60km', tip: '返回市区后推荐购买腊驴肉特产'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '太行山大峡谷'}), (ac:Accommodation {name: '长治益东国际酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '65km', tip: '位于市中心，适合长途游览后休整'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '老顶山国家森林公园'}), (ac:Accommodation {name: '长治宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '6km', tip: '靠近森林公园，休闲出行便利'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '长治'}), (t:Transportation)
               WHERE t.name IN ['长治公交', '长治东站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '长治公交'}), (t2:Transportation {name: '长治东站'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '公交直达高铁站，方便前往太原、郑州等地'}]->(t2)
           """)

        print("长治旅游数据导入完成！")

    def import_jincheng_data(self):
        """导入晋城旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (jc:City {name: '晋城', level: '地级市', description: '山西省地级市，太行山城，煤炭与煤化工基地'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (huangcheng_xiangfu:Attraction {name: '皇城相府', type: '人文景观', rating: 4.7, opening_hours: '8:00 - 17:30'}),
               (wangmangling:Attraction {name: '王莽岭', type: '自然景观', rating: 4.6, opening_hours: '7:30 - 17:30'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (jincheng_chaoliangfen:Food {name: '晋城炒凉粉', type: '地方小吃', price_range: '低', description: '口感爽滑，香辣可口'}),
               (yangcheng_shaogan:Food {name: '阳城烧肝', type: '传统美食', price_range: '中低', description: '外焦里嫩，风味独特'}),
               (guomao_hotel:Accommodation {name: '晋城国贸大酒店', type: '五星级酒店', price_range: '高', rating: 4.6}),
               (jinlian_hotel:Accommodation {name: '晋城金辇大酒店', type: '四星级酒店', price_range: '中', rating: 4.4}),
               (jc_bus:Transportation {name: '晋城公交', type: '公交', route: '覆盖市区', price: '1-2元'}),
               (jc_east_railway:Transportation {name: '晋城东站', type: '高铁站', route: '通往郑州等地', price: '根据里程'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '晋城'})
               WHERE a.name IN ['皇城相府', '王莽岭']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '晋城'}), (f:Food)
               WHERE f.name IN ['晋城炒凉粉', '阳城烧肝']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '皇城相府'}), (f:Food {name: '晋城炒凉粉'})
               CREATE (a)-[:NEAR_FOOD {distance: '1km', tip: '相府景区商业街可品尝特色炒凉粉'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '皇城相府'}), (f:Food {name: '阳城烧肝'})
               CREATE (a)-[:NEAR_FOOD {distance: '3km', tip: '周边乡镇餐馆可体验传统烧肝'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '王莽岭'}), (f:Food {name: '晋城炒凉粉'})
               CREATE (a)-[:NEAR_FOOD {distance: '20km', tip: '下山后前往市区品尝地道小吃'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '皇城相府'}), (ac:Accommodation {name: '晋城国贸大酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '50km'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '王莽岭'}), (ac:Accommodation {name: '晋城金辇大酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '45km', tip: '适合自然景观游览后休整'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '晋城'}), (t:Transportation)
               WHERE t.name IN ['晋城公交', '晋城东站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '晋城公交'}), (t2:Transportation {name: '晋城东站'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '公交直达高铁站，方便前往郑州、太原等地'}]->(t2)
           """)

        print("晋城旅游数据导入完成！")

    def import_shuozhou_data(self):
        """导入朔州旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (sz:City {name: '朔州', level: '地级市', description: '山西省地级市，边塞文化名城，重要能源基地'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (yingxian_muta:Attraction {name: '应县木塔', type: '人文景观', rating: 4.7, opening_hours: '8:30 - 17:30'}),
               (chongfu_si:Attraction {name: '崇福寺', type: '人文景观', rating: 4.5, opening_hours: '8:00 - 17:00'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (shuozhou_yangza:Food {name: '朔州羊杂', type: '地方小吃', price_range: '低', description: '汤鲜味美，暖胃驱寒'}),
               (youyu_yuebing:Food {name: '右玉月饼', type: '传统糕点', price_range: '低', description: '皮薄馅足，香甜可口'}),
               (sijiping_shuo:Accommodation {name: '朔州四季平朔大酒店', type: '四星级酒店', price_range: '中', rating: 4.4}),
               (shuozhou_hotel:Accommodation {name: '朔州宾馆', type: '商务酒店', price_range: '中低', rating: 4.2}),
               (sz_bus:Transportation {name: '朔州公交', type: '公交', route: '覆盖市区', price: '1-2元'}),
               (sz_railway:Transportation {name: '朔州站', type: '火车站', route: '通往大同等地', price: '根据里程'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '朔州'})
               WHERE a.name IN ['应县木塔', '崇福寺']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '朔州'}), (f:Food)
               WHERE f.name IN ['朔州羊杂', '右玉月饼']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '应县木塔'}), (f:Food {name: '朔州羊杂'})
               CREATE (a)-[:NEAR_FOOD {distance: '1km', tip: '木塔周边餐馆可品尝正宗羊杂'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '应县木塔'}), (f:Food {name: '右玉月饼'})
               CREATE (a)-[:NEAR_FOOD {distance: '2km', tip: '景区特产店有售传统月饼'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '崇福寺'}), (f:Food {name: '朔州羊杂'})
               CREATE (a)-[:NEAR_FOOD {distance: '1.5km', tip: '寺院周边小吃摊可体验特色羊杂'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '应县木塔'}), (ac:Accommodation {name: '朔州四季平朔大酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '70km'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '崇福寺'}), (ac:Accommodation {name: '朔州宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '2km', tip: '毗邻历史文化街区，出行便利'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '朔州'}), (t:Transportation)
               WHERE t.name IN ['朔州公交', '朔州站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '朔州公交'}), (t2:Transportation {name: '朔州站'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '公交直达火车站，方便前往大同、太原等地'}]->(t2)
           """)

        print("朔州旅游数据导入完成！")

    def import_jinzhong_data(self):
        """导入晋中旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (jz:City {name: '晋中', level: '地级市', description: '山西省地级市，晋商文化发祥地，历史文化名城'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (pingyao_oldtown:Attraction {name: '平遥古城', type: '人文景观', rating: 4.8, opening_hours: '全天开放'}),
               (qiaojiadayuan:Attraction {name: '乔家大院', type: '人文景观', rating: 4.7, opening_hours: '8:00 - 17:30'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (pingyao_niurou:Food {name: '平遥牛肉', type: '地方特产', price_range: '中', description: '肉质鲜嫩，香味浓郁'}),
               (taigu_bing:Food {name: '太谷饼', type: '传统糕点', price_range: '低', description: '酥软香甜，口感独特'}),
               (pingyao_jinzhai:Accommodation {name: '平遥锦宅酒店', type: '精品酒店', price_range: '中高', rating: 4.7}),
               (jinzhong_wanhua:Accommodation {name: '晋中万豪酒店', type: '五星级酒店', price_range: '高', rating: 4.5}),
               (jz_bus:Transportation {name: '晋中公交', type: '公交', route: '覆盖市区', price: '1-2元'}),
               (pingyao_railway:Transportation {name: '平遥古城站', type: '高铁站', route: '通往太原等地', price: '根据里程'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '晋中'})
               WHERE a.name IN ['平遥古城', '乔家大院']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '晋中'}), (f:Food)
               WHERE f.name IN ['平遥牛肉', '太谷饼']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '平遥古城'}), (f:Food {name: '平遥牛肉'})
               CREATE (a)-[:NEAR_FOOD {distance: '0.3km', tip: '古城内老字号店铺可品尝正宗牛肉'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '平遥古城'}), (f:Food {name: '太谷饼'})
               CREATE (a)-[:NEAR_FOOD {distance: '0.5km', tip: '古城商业街有售传统太谷饼'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '乔家大院'}), (f:Food {name: '平遥牛肉'})
               CREATE (a)-[:NEAR_FOOD {distance: '40km', tip: '前往平遥古城途中可购买特产牛肉'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '平遥古城'}), (ac:Accommodation {name: '平遥锦宅酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '0.8km', tip: '位于古城内，体验晋商民居特色'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '乔家大院'}), (ac:Accommodation {name: '晋中万豪酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '35km'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '晋中'}), (t:Transportation)
               WHERE t.name IN ['晋中公交', '平遥古城站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '晋中公交'}), (t2:Transportation {name: '平遥古城站'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '公交专线连接市区与高铁站，方便游览平遥古城'}]->(t2)
           """)

        print("晋中旅游数据导入完成！")

    def import_yuncheng_data(self):
        """导入运城旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (yc:City {name: '运城', level: '地级市', description: '山西省地级市，关公故里，华夏文明发祥地之一'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (xiezhou_guandimiao:Attraction {name: '解州关帝庙', type: '人文景观', rating: 4.7, opening_hours: '8:00 - 17:30'}),
               (yuncheng_yanhu:Attraction {name: '运城盐湖', type: '自然景观', rating: 4.5, opening_hours: '8:30 - 18:00'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (wenxi_zhubing:Food {name: '闻喜煮饼', type: '传统小吃', price_range: '低', description: '外酥里嫩，甜而不腻'}),
               (yuncheng_yangroupaomo:Food {name: '运城羊肉泡馍', type: '地方特色', price_range: '中低', description: '汤浓肉烂，馍筋道'}),
               (jinxin_hotel:Accommodation {name: '运城金鑫大酒店', type: '五星级酒店', price_range: '高', rating: 4.6}),
               (shenhang_international:Accommodation {name: '运城深航国际酒店', type: '五星级酒店', price_range: '高', rating: 4.5}),
               (yc_bus:Transportation {name: '运城公交', type: '公交', route: '覆盖市区', price: '1-2元'}),
               (yc_north_railway:Transportation {name: '运城北站', type: '高铁站', route: '通往西安等地', price: '根据里程'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '运城'})
               WHERE a.name IN ['解州关帝庙', '运城盐湖']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '运城'}), (f:Food)
               WHERE f.name IN ['闻喜煮饼', '运城羊肉泡馍']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '解州关帝庙'}), (f:Food {name: '闻喜煮饼'})
               CREATE (a)-[:NEAR_FOOD {distance: '3km', tip: '景区周边特产店有售传统煮饼'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '解州关帝庙'}), (f:Food {name: '运城羊肉泡馍'})
               CREATE (a)-[:NEAR_FOOD {distance: '2km', tip: '关帝庙附近餐馆可品尝特色泡馍'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '运城盐湖'}), (f:Food {name: '闻喜煮饼'})
               CREATE (a)-[:NEAR_FOOD {distance: '15km', tip: '返回市区后可购买传统煮饼'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '解州关帝庙'}), (ac:Accommodation {name: '运城金鑫大酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '20km', tip: '适合文化游览后休整'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '运城盐湖'}), (ac:Accommodation {name: '运城深航国际酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '10km', tip: '靠近盐湖景区，出行便利'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '运城'}), (t:Transportation)
               WHERE t.name IN ['运城公交', '运城北站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '运城公交'}), (t2:Transportation {name: '运城北站'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '公交直达高铁站，方便前往西安、太原等地'}]->(t2)
           """)

        print("运城旅游数据导入完成！")

    def import_xinzhou_data(self):
        """导入忻州旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (xz:City {name: '忻州', level: '地级市', description: '山西省地级市，佛教圣地，晋北锁钥'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (wutaishan:Attraction {name: '五台山', type: '人文景观', rating: 4.8, opening_hours: '全天开放'}),
               (yanmenguan:Attraction {name: '雁门关', type: '人文景观', rating: 4.6, opening_hours: '8:00 - 18:00'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (xinzhou_wasu:Food {name: '忻州瓦酥', type: '传统糕点', price_range: '低', description: '酥脆香甜，入口即化'}),
               (dingxiang_zhengrou:Food {name: '定襄蒸肉', type: '地方特色', price_range: '中低', description: '肉质鲜嫩，香味浓郁'}),
               (fanhua_hotel:Accommodation {name: '忻州泛华大酒店', type: '四星级酒店', price_range: '中', rating: 4.5}),
               (wutaishan_wanhua:Accommodation {name: '五台山万豪酒店', type: '五星级酒店', price_range: '高', rating: 4.6}),
               (xz_bus:Transportation {name: '忻州公交', type: '公交', route: '覆盖市区', price: '1-2元'}),
               (xz_west_railway:Transportation {name: '忻州西站', type: '高铁站', route: '通往太原等地', price: '根据里程'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '忻州'})
               WHERE a.name IN ['五台山', '雁门关']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '忻州'}), (f:Food)
               WHERE f.name IN ['忻州瓦酥', '定襄蒸肉']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '五台山'}), (f:Food {name: '忻州瓦酥'})
               CREATE (a)-[:NEAR_FOOD {distance: '5km', tip: '台怀镇商业街可购买传统瓦酥'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '五台山'}), (f:Food {name: '定襄蒸肉'})
               CREATE (a)-[:NEAR_FOOD {distance: '80km', tip: '返回忻州城区后可品尝正宗蒸肉'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '雁门关'}), (f:Food {name: '定襄蒸肉'})
               CREATE (a)-[:NEAR_FOOD {distance: '60km', tip: '前往定襄县途中可体验特色蒸肉'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '五台山'}), (ac:Accommodation {name: '五台山万豪酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '3km', tip: '位于景区内，方便佛教文化体验'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '雁门关'}), (ac:Accommodation {name: '忻州泛华大酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '85km', tip: '位于城区，适合边塞游览后休整'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '忻州'}), (t:Transportation)
               WHERE t.name IN ['忻州公交', '忻州西站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '忻州公交'}), (t2:Transportation {name: '忻州西站'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '公交直达高铁站，方便前往太原、大同等地'}]->(t2)
           """)

        print("忻州旅游数据导入完成！")

    def import_linfen_data(self):
        """导入临汾旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (lf:City {name: '临汾', level: '地级市', description: '山西省地级市，华夏民族发祥地之一，尧都'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (yaomiao:Attraction {name: '尧庙', type: '人文景观', rating: 4.6, opening_hours: '8:00 - 17:30'}),
               (hukou_pubu:Attraction {name: '壶口瀑布', type: '自然景观', rating: 4.8, opening_hours: '7:00 - 18:00'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (linfen_niuwanzi:Food {name: '临汾牛肉丸子面', type: '地方小吃', price_range: '低', description: '面条筋道，汤鲜味美'}),
               (wujia_xunrou:Food {name: '吴家熏肉', type: '传统美食', price_range: '中低', description: '色泽红亮，熏香浓郁'}),
               (jindu_garden:Accommodation {name: '临汾金都花园大酒店', type: '五星级酒店', price_range: '高', rating: 4.6}),
               (linfen_hotel:Accommodation {name: '临汾宾馆', type: '四星级酒店', price_range: '中', rating: 4.4}),
               (lf_bus:Transportation {name: '临汾公交', type: '公交', route: '覆盖市区', price: '1-2元'}),
               (lf_west_railway:Transportation {name: '临汾西站', type: '高铁站', route: '通往太原等地', price: '根据里程'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '临汾'})
               WHERE a.name IN ['尧庙', '壶口瀑布']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '临汾'}), (f:Food)
               WHERE f.name IN ['临汾牛肉丸子面', '吴家熏肉']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '尧庙'}), (f:Food {name: '临汾牛肉丸子面'})
               CREATE (a)-[:NEAR_FOOD {distance: '2km', tip: '尧庙周边餐馆可品尝特色丸子面'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '尧庙'}), (f:Food {name: '吴家熏肉'})
               CREATE (a)-[:NEAR_FOOD {distance: '3km', tip: '市区老字号店铺可购买传统熏肉'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '壶口瀑布'}), (f:Food {name: '临汾牛肉丸子面'})
               CREATE (a)-[:NEAR_FOOD {distance: '100km', tip: '返回市区后推荐品尝地道面食'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '尧庙'}), (ac:Accommodation {name: '临汾宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '4km', tip: '靠近尧庙景区，方便文化游览'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '壶口瀑布'}), (ac:Accommodation {name: '临汾金都花园大酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '95km', tip: '位于市中心，适合长途游览后休整'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '临汾'}), (t:Transportation)
               WHERE t.name IN ['临汾公交', '临汾西站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '临汾公交'}), (t2:Transportation {name: '临汾西站'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '公交直达高铁站，方便前往太原、西安等地'}]->(t2)
           """)

        print("临汾旅游数据导入完成！")

    def import_lvliang_data(self):
        """导入吕梁旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (ll:City {name: '吕梁', level: '地级市', description: '山西省地级市，革命老区，红枣之乡'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (beiwudangshan:Attraction {name: '北武当山', type: '自然景观', rating: 4.5, opening_hours: '8:00 - 17:30'}),
               (qikou_guzhen:Attraction {name: '碛口古镇', type: '人文景观', rating: 4.6, opening_hours: '全天开放'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (liulin_wantuo:Food {name: '柳林碗托', type: '地方小吃', price_range: '低', description: '口感爽滑，酸辣开胃'}),
               (lvliang_hongzao:Food {name: '吕梁红枣', type: '地方特产', price_range: '低', description: '肉厚核小，香甜可口'}),
               (lvliang_international:Accommodation {name: '吕梁国际宾馆', type: '四星级酒店', price_range: '中', rating: 4.4}),
               (donggucang_hotel:Accommodation {name: '吕梁东谷仓酒店', type: '商务酒店', price_range: '中低', rating: 4.2}),
               (ll_bus:Transportation {name: '吕梁公交', type: '公交', route: '覆盖市区', price: '1-2元'}),
               (ll_railway:Transportation {name: '吕梁站', type: '火车站', route: '通往太原等地', price: '根据里程'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '吕梁'})
               WHERE a.name IN ['北武当山', '碛口古镇']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '吕梁'}), (f:Food)
               WHERE f.name IN ['柳林碗托', '吕梁红枣']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '碛口古镇'}), (f:Food {name: '柳林碗托'})
               CREATE (a)-[:NEAR_FOOD {distance: '1km', tip: '古镇街巷可品尝正宗碗托'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '碛口古镇'}), (f:Food {name: '吕梁红枣'})
               CREATE (a)-[:NEAR_FOOD {distance: '2km', tip: '古镇集市有售优质红枣'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '北武当山'}), (f:Food {name: '柳林碗托'})
               CREATE (a)-[:NEAR_FOOD {distance: '50km', tip: '下山后前往柳林县品尝特色碗托'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '北武当山'}), (ac:Accommodation {name: '吕梁国际宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '60km', tip: '适合山地游览后休整'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '碛口古镇'}), (ac:Accommodation {name: '吕梁东谷仓酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '55km', tip: '返回市区后便捷住宿选择'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '吕梁'}), (t:Transportation)
               WHERE t.name IN ['吕梁公交', '吕梁站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '吕梁公交'}), (t2:Transportation {name: '吕梁站'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '公交直达火车站，方便前往太原、西安等地'}]->(t2)
           """)

        print("吕梁旅游数据导入完成！")

    def import_gujiao_data(self):
        """导入古交旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (gj:City {name: '古交', level: '县级市', description: '山西省县级市，太原代管，重要焦煤生产基地'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (jinniu_forest:Attraction {name: '金牛森林公园', type: '自然景观', rating: 4.3, opening_hours: '全天开放'}),
               (huye_mountain:Attraction {name: '狐爷山', type: '自然景观', rating: 4.2, opening_hours: '8:00 - 17:00'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (gujiao_youmianer:Food {name: '古交油面儿', type: '地方小吃', price_range: '低', description: '外脆里软，香甜可口'}),
               (gujiao_dunyangrou:Food {name: '古交炖羊肉', type: '地方特色', price_range: '中', description: '肉质鲜嫩，汤味浓郁'}),
               (meijiao_hotel:Accommodation {name: '古交煤焦大酒店', type: '三星级酒店', price_range: '中低', rating: 4.2}),
               (gujiao_hotel:Accommodation {name: '古交宾馆', type: '商务酒店', price_range: '中低', rating: 4.1}),
               (gj_bus:Transportation {name: '古交公交', type: '公交', route: '覆盖市区', price: '1-2元'}),
               (gj_bus_station:Transportation {name: '古交汽车站', type: '客运站', route: '通往太原等地', price: '根据里程'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '古交'})
               WHERE a.name IN ['金牛森林公园', '狐爷山']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '古交'}), (f:Food)
               WHERE f.name IN ['古交油面儿', '古交炖羊肉']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '金牛森林公园'}), (f:Food {name: '古交油面儿'})
               CREATE (a)-[:NEAR_FOOD {distance: '1.5km', tip: '公园周边小吃摊可品尝油面儿'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '金牛森林公园'}), (f:Food {name: '古交炖羊肉'})
               CREATE (a)-[:NEAR_FOOD {distance: '2km', tip: '市区餐馆可体验特色炖羊肉'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '狐爷山'}), (f:Food {name: '古交炖羊肉'})
               CREATE (a)-[:NEAR_FOOD {distance: '30km', tip: '返回市区后推荐品尝正宗炖羊肉'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '金牛森林公园'}), (ac:Accommodation {name: '古交煤焦大酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '3km', tip: '靠近森林公园，休闲便利'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '狐爷山'}), (ac:Accommodation {name: '古交宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '32km', tip: '适合山地游览后休整'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '古交'}), (t:Transportation)
               WHERE t.name IN ['古交公交', '古交汽车站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '古交公交'}), (t2:Transportation {name: '古交汽车站'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '公交直达汽车站，方便前往太原市区'}]->(t2)
           """)

        print("古交旅游数据导入完成！")

    def import_gaoping_data(self):
        """导入高平旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (gp:City {name: '高平', level: '县级市', description: '山西省县级市，晋城代管，炎帝文化发祥地'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (yandiling:Attraction {name: '炎帝陵', type: '人文景观', rating: 4.5, opening_hours: '8:30 - 17:30'}),
               (yangtoushan:Attraction {name: '羊头山石窟', type: '人文景观', rating: 4.4, opening_hours: '8:00 - 17:00'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (gaoping_shidawan:Food {name: '高平十大碗', type: '地方特色', price_range: '中', description: '宴席菜肴，丰富多样'}),
               (gaoping_shaodoufu:Food {name: '高平烧豆腐', type: '传统小吃', price_range: '低', description: '外焦里嫩，酱香浓郁'}),
               (jiulong_hotel:Accommodation {name: '高平九龙大酒店', type: '三星级酒店', price_range: '中低', rating: 4.3}),
               (yandi_hotel:Accommodation {name: '高平炎帝宾馆', type: '商务酒店', price_range: '中低', rating: 4.2}),
               (gp_bus:Transportation {name: '高平公交', type: '公交', route: '覆盖市区', price: '1-2元'}),
               (gp_east_railway:Transportation {name: '高平东站', type: '高铁站', route: '通往晋城等地', price: '根据里程'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '高平'})
               WHERE a.name IN ['炎帝陵', '羊头山石窟']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '高平'}), (f:Food)
               WHERE f.name IN ['高平十大碗', '高平烧豆腐']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '炎帝陵'}), (f:Food {name: '高平十大碗'})
               CREATE (a)-[:NEAR_FOOD {distance: '3km', tip: '景区周边餐馆可体验传统宴席'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '炎帝陵'}), (f:Food {name: '高平烧豆腐'})
               CREATE (a)-[:NEAR_FOOD {distance: '2.5km', tip: '陵前小吃摊可品尝特色烧豆腐'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '羊头山石窟'}), (f:Food {name: '高平烧豆腐'})
               CREATE (a)-[:NEAR_FOOD {distance: '8km', tip: '下山后乡镇餐馆可体验地道小吃'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '炎帝陵'}), (ac:Accommodation {name: '高平炎帝宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '4km', tip: '呼应炎帝文化主题，出行便利'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '羊头山石窟'}), (ac:Accommodation {name: '高平九龙大酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '10km', tip: '适合文化游览后休整'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '高平'}), (t:Transportation)
               WHERE t.name IN ['高平公交', '高平东站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '高平公交'}), (t2:Transportation {name: '高平东站'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '公交直达高铁站，方便前往晋城、郑州等地'}]->(t2)
           """)

        print("高平旅游数据导入完成！")

    def import_huairen_data(self):
        """导入怀仁旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (hr:City {name: '怀仁', level: '县级市', description: '山西省县级市，朔州代管，中国陶瓷之乡'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (jinshatan:Attraction {name: '金沙滩生态旅游区', type: '人文景观', rating: 4.4, opening_hours: '8:30 - 17:30'}),
               (qingliangshan:Attraction {name: '清凉山', type: '自然景观', rating: 4.3, opening_hours: '8:00 - 17:00'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (huairen_yangza:Food {name: '怀仁羊杂', type: '地方小吃', price_range: '低', description: '汤鲜味美，暖胃驱寒'}),
               (huairen_tangganlu:Food {name: '怀仁糖干炉', type: '传统糕点', price_range: '低', description: '酥脆香甜，风味独特'}),
               (guoyi_hotel:Accommodation {name: '怀仁国益大酒店', type: '三星级酒店', price_range: '中低', rating: 4.3}),
               (huairen_hotel:Accommodation {name: '怀仁宾馆', type: '商务酒店', price_range: '中低', rating: 4.1}),
               (hr_bus:Transportation {name: '怀仁公交', type: '公交', route: '覆盖市区', price: '1-2元'}),
               (hr_east_railway:Transportation {name: '怀仁东站', type: '高铁站', route: '通往大同等地', price: '根据里程'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '怀仁'})
               WHERE a.name IN ['金沙滩生态旅游区', '清凉山']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '怀仁'}), (f:Food)
               WHERE f.name IN ['怀仁羊杂', '怀仁糖干炉']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '金沙滩生态旅游区'}), (f:Food {name: '怀仁羊杂'})
               CREATE (a)-[:NEAR_FOOD {distance: '2km', tip: '景区周边餐馆可品尝正宗羊杂'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '金沙滩生态旅游区'}), (f:Food {name: '怀仁糖干炉'})
               CREATE (a)-[:NEAR_FOOD {distance: '3km', tip: '旅游区商业街有售传统糖干炉'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '清凉山'}), (f:Food {name: '怀仁羊杂'})
               CREATE (a)-[:NEAR_FOOD {distance: '15km', tip: '下山后市区餐馆可体验特色羊杂'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '金沙滩生态旅游区'}), (ac:Accommodation {name: '怀仁国益大酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '18km', tip: '适合文化旅游后休整'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '清凉山'}), (ac:Accommodation {name: '怀仁宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '16km', tip: '靠近市区，出行便利'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '怀仁'}), (t:Transportation)
               WHERE t.name IN ['怀仁公交', '怀仁东站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '怀仁公交'}), (t2:Transportation {name: '怀仁东站'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '公交直达高铁站，方便前往大同、朔州等地'}]->(t2)
           """)

        print("怀仁旅游数据导入完成！")

    def import_jiexiu_data(self):
        """导入介休旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (jx:City {name: '介休', level: '县级市', description: '山西省县级市，晋中代管，清明寒食文化发源地'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (mianshan:Attraction {name: '绵山', type: '自然+人文景观', rating: 4.7, opening_hours: '7:30 - 17:30'}),
               (zhangbi_gubao:Attraction {name: '张壁古堡', type: '人文景观', rating: 4.5, opening_hours: '8:00 - 17:00'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (jiexiu_dandanmian:Food {name: '介休担担面', type: '地方小吃', price_range: '低', description: '面条筋道，调料香浓'}),
               (guanxian_tang:Food {name: '贯馅糖', type: '传统糕点', price_range: '低', description: '酥脆香甜，糖馅饱满'}),
               (jiexiu_mianshan:Accommodation {name: '介休绵山酒店', type: '三星级酒店', price_range: '中低', rating: 4.4}),
               (jiexiu_hotel:Accommodation {name: '介休宾馆', type: '商务酒店', price_range: '中低', rating: 4.2}),
               (jx_bus:Transportation {name: '介休公交', type: '公交', route: '覆盖市区', price: '1-2元'}),
               (jx_east_railway:Transportation {name: '介休东站', type: '高铁站', route: '通往太原等地', price: '根据里程'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '介休'})
               WHERE a.name IN ['绵山', '张壁古堡']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '介休'}), (f:Food)
               WHERE f.name IN ['介休担担面', '贯馅糖']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '绵山'}), (f:Food {name: '介休担担面'})
               CREATE (a)-[:NEAR_FOOD {distance: '2km', tip: '景区服务区可品尝特色担担面'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '绵山'}), (f:Food {name: '贯馅糖'})
               CREATE (a)-[:NEAR_FOOD {distance: '3km', tip: '景区特产店有售传统贯馅糖'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '张壁古堡'}), (f:Food {name: '介休担担面'})
               CREATE (a)-[:NEAR_FOOD {distance: '15km', tip: '返回市区后可体验正宗担担面'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '绵山'}), (ac:Accommodation {name: '介休绵山酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '5km', tip: '毗邻绵山景区，方便文化体验'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '张壁古堡'}), (ac:Accommodation {name: '介休宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '16km', tip: '位于市区，适合古堡游览后休整'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '介休'}), (t:Transportation)
               WHERE t.name IN ['介休公交', '介休东站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '介休公交'}), (t2:Transportation {name: '介休东站'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '公交直达高铁站，方便前往太原、晋中等地'}]->(t2)
           """)

        print("介休旅游数据导入完成！")

    def import_yongji_data(self):
        """导入永济旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (yj:City {name: '永济', level: '县级市', description: '山西省县级市，运城代管，唐代中都，爱情文化圣地'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (pujusi:Attraction {name: '普救寺', type: '人文景观', rating: 4.6, opening_hours: '8:00 - 17:30'}),
               (guanquelou:Attraction {name: '鹳雀楼', type: '人文景观', rating: 4.7, opening_hours: '8:30 - 17:00'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (yongji_niuroujiaozi:Food {name: '永济牛肉饺子', type: '地方特色', price_range: '中低', description: '皮薄馅大，汤汁鲜美'}),
               (yongji_chemian:Food {name: '永济扯面', type: '传统面食', price_range: '低', description: '面条筋道，卤汁香浓'}),
               (haina_hotel:Accommodation {name: '永济海纳大酒店', type: '三星级酒店', price_range: '中低', rating: 4.4}),
               (yongji_hotel:Accommodation {name: '永济宾馆', type: '商务酒店', price_range: '中低', rating: 4.2}),
               (yj_bus:Transportation {name: '永济公交', type: '公交', route: '覆盖市区', price: '1-2元'}),
               (yj_north_railway:Transportation {name: '永济北站', type: '高铁站', route: '通往西安等地', price: '根据里程'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '永济'})
               WHERE a.name IN ['普救寺', '鹳雀楼']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '永济'}), (f:Food)
               WHERE f.name IN ['永济牛肉饺子', '永济扯面']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '普救寺'}), (f:Food {name: '永济牛肉饺子'})
               CREATE (a)-[:NEAR_FOOD {distance: '1.5km', tip: '寺外餐馆可品尝特色牛肉饺子'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '普救寺'}), (f:Food {name: '永济扯面'})
               CREATE (a)-[:NEAR_FOOD {distance: '2km', tip: '景区周边面馆可体验传统扯面'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '鹳雀楼'}), (f:Food {name: '永济扯面'})
               CREATE (a)-[:NEAR_FOOD {distance: '30km', tip: '返回市区后推荐品尝正宗扯面'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '普救寺'}), (ac:Accommodation {name: '永济海纳大酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '3km', tip: '靠近爱情文化景区，氛围契合'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '鹳雀楼'}), (ac:Accommodation {name: '永济宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '28km', tip: '位于市区，适合历史景观游览后休整'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '永济'}), (t:Transportation)
               WHERE t.name IN ['永济公交', '永济北站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '永济公交'}), (t2:Transportation {name: '永济北站'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '公交直达高铁站，方便前往西安、运城等地'}]->(t2)
           """)

        print("永济旅游数据导入完成！")

    def import_hejin_data(self):
        """导入河津旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (hj:City {name: '河津', level: '县级市', description: '山西省县级市，运城代管，大禹治水、鱼跃龙门故事发生地'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (longmen:Attraction {name: '龙门', type: '自然+人文景观', rating: 4.5, opening_hours: '8:00 - 17:30'}),
               (zhenwu_miao:Attraction {name: '真武庙', type: '人文景观', rating: 4.3, opening_hours: '8:30 - 17:00'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (hejin_paopaoyougao:Food {name: '河津泡泡油糕', type: '地方小吃', price_range: '低', description: '外脆里糯，甜香适口'}),
               (hejin_huangheliyu:Food {name: '河津黄河鲤鱼', type: '地方特色', price_range: '中', description: '肉质鲜嫩，营养丰富'}),
               (hejin_international:Accommodation {name: '河津国际酒店', type: '三星级酒店', price_range: '中低', rating: 4.3}),
               (longmen_dasha:Accommodation {name: '河津龙门大厦', type: '商务酒店', price_range: '中低', rating: 4.2}),
               (hj_bus:Transportation {name: '河津公交', type: '公交', route: '覆盖市区', price: '1-2元'}),
               (hj_railway:Transportation {name: '河津站', type: '火车站', route: '通往运城等地', price: '根据里程'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '河津'})
               WHERE a.name IN ['龙门', '真武庙']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '河津'}), (f:Food)
               WHERE f.name IN ['河津泡泡油糕', '河津黄河鲤鱼']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '龙门'}), (f:Food {name: '河津黄河鲤鱼'})
               CREATE (a)-[:NEAR_FOOD {distance: '1km', tip: '龙门景区周边餐馆可品尝正宗黄河鲤鱼'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '龙门'}), (f:Food {name: '河津泡泡油糕'})
               CREATE (a)-[:NEAR_FOOD {distance: '2km', tip: '景区商业街有售特色泡泡油糕'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '真武庙'}), (f:Food {name: '河津泡泡油糕'})
               CREATE (a)-[:NEAR_FOOD {distance: '3km', tip: '下山后市区小吃店可体验传统油糕'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '龙门'}), (ac:Accommodation {name: '河津龙门大厦'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '5km', tip: '呼应龙门文化主题，观景便利'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '真武庙'}), (ac:Accommodation {name: '河津国际酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '4km', tip: '位于城区，适合文化游览后休整'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '河津'}), (t:Transportation)
               WHERE t.name IN ['河津公交', '河津站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '河津公交'}), (t2:Transportation {name: '河津站'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '公交直达火车站，方便前往运城、西安等地'}]->(t2)
           """)

        print("河津旅游数据导入完成！")

    def import_yuanping_data(self):
        """导入原平旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (yp:City {name: '原平', level: '县级市', description: '山西省县级市，忻州代管，晋北交通枢纽'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (tianya_shan:Attraction {name: '天涯山', type: '自然景观', rating: 4.4, opening_hours: '8:00 - 17:30'}),
               (wufeng_shan:Attraction {name: '五峰山', type: '自然景观', rating: 4.3, opening_hours: '7:30 - 17:00'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (yuanping_guokui:Food {name: '原平锅盔', type: '传统面食', price_range: '低', description: '外脆内软，麦香浓郁'}),
               (yuanping_xunji:Food {name: '原平熏鸡', type: '地方特色', price_range: '中低', description: '色泽金黄，熏香入味'}),
               (yuanping_hotel:Accommodation {name: '原平宾馆', type: '三星级酒店', price_range: '中低', rating: 4.3}),
               (yuanda_dasha:Accommodation {name: '原平铁道大厦', type: '商务酒店', price_range: '中低', rating: 4.1}),
               (yp_bus:Transportation {name: '原平公交', type: '公交', route: '覆盖市区', price: '1-2元'}),
               (yp_west_railway:Transportation {name: '原平西站', type: '高铁站', route: '通往太原等地', price: '根据里程'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '原平'})
               WHERE a.name IN ['天涯山', '五峰山']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '原平'}), (f:Food)
               WHERE f.name IN ['原平锅盔', '原平熏鸡']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '天涯山'}), (f:Food {name: '原平锅盔'})
               CREATE (a)-[:NEAR_FOOD {distance: '2km', tip: '景区服务区可品尝传统锅盔'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '天涯山'}), (f:Food {name: '原平熏鸡'})
               CREATE (a)-[:NEAR_FOOD {distance: '3km', tip: '景区周边餐馆可体验特色熏鸡'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '五峰山'}), (f:Food {name: '原平锅盔'})
               CREATE (a)-[:NEAR_FOOD {distance: '15km', tip: '下山后市区店铺可购买正宗锅盔'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '天涯山'}), (ac:Accommodation {name: '原平宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '8km', tip: '适合山地游览后休整'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '五峰山'}), (ac:Accommodation {name: '原平铁道大厦'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '20km', tip: '靠近交通枢纽，出行便利'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '原平'}), (t:Transportation)
               WHERE t.name IN ['原平公交', '原平西站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '原平公交'}), (t2:Transportation {name: '原平西站'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '公交直达高铁站，方便前往太原、大同等地'}]->(t2)
           """)

        print("原平旅游数据导入完成！")

    def import_houma_data(self):
        """导入侯马旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (hm:City {name: '侯马', level: '县级市', description: '山西省县级市，临汾代管，晋南交通枢纽，晋文化发祥地'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (jin_gu遗址:Attraction {name: '侯马晋国遗址', type: '人文景观', rating: 4.5, opening_hours: '8:30 - 17:00'}),
               (pengzhen_故居:Attraction {name: '彭真故居', type: '人文景观', rating: 4.4, opening_hours: '9:00 - 16:30'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (houma_saomian:Food {name: '侯马臊子面', type: '地方小吃', price_range: '低', description: '面条筋道，臊子香浓'}),
               (houma_yangrouguo:Food {name: '侯马羊肉锅', type: '地方特色', price_range: '中', description: '汤鲜肉嫩，暖胃驱寒'}),
               (jinshiji_hotel:Accommodation {name: '侯马金世纪大酒店', type: '三星级酒店', price_range: '中低', rating: 4.3}),
               (tongsheng_hotel:Accommodation {name: '侯马通盛商务酒店', type: '商务酒店', price_range: '中低', rating: 4.2}),
               (hm_bus:Transportation {name: '侯马公交', type: '公交', route: '覆盖市区', price: '1-2元'}),
               (hm_west_railway:Transportation {name: '侯马西站', type: '高铁站', route: '通往太原、西安等地', price: '根据里程'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '侯马'})
               WHERE a.name IN ['侯马晋国遗址', '彭真故居']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '侯马'}), (f:Food)
               WHERE f.name IN ['侯马臊子面', '侯马羊肉锅']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '侯马晋国遗址'}), (f:Food {name: '侯马臊子面'})
               CREATE (a)-[:NEAR_FOOD {distance: '2.5km', tip: '遗址周边餐馆可品尝特色臊子面'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '侯马晋国遗址'}), (f:Food {name: '侯马羊肉锅'})
               CREATE (a)-[:NEAR_FOOD {distance: '3km', tip: '景区附近餐馆可体验传统羊肉锅'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '彭真故居'}), (f:Food {name: '侯马臊子面'})
               CREATE (a)-[:NEAR_FOOD {distance: '1.5km', tip: '故居周边面馆可品尝地道臊子面'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '侯马晋国遗址'}), (ac:Accommodation {name: '侯马金世纪大酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '4km', tip: '适合晋文化研学后休整'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '彭真故居'}), (ac:Accommodation {name: '侯马通盛商务酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '2km', tip: '靠近市区，方便红色文化体验'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '侯马'}), (t:Transportation)
               WHERE t.name IN ['侯马公交', '侯马西站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '侯马公交'}), (t2:Transportation {name: '侯马西站'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '公交直达高铁站，强化晋南交通枢纽功能'}]->(t2)
           """)

        print("侯马旅游数据导入完成！")

    def import_huozhou_data(self):
        """导入霍州旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (hz:City {name: '霍州', level: '县级市', description: '山西省县级市，临汾代管，中国年馍之乡'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (huozhou_shu:Attraction {name: '霍州署', type: '人文景观', rating: 4.5, opening_hours: '8:30 - 17:00'}),
               (qiliyu:Attraction {name: '七里峪', type: '自然景观', rating: 4.4, opening_hours: '8:00 - 17:30'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (huozhou_nianmo:Food {name: '霍州年馍', type: '地方特色', price_range: '低', description: '造型多样，寓意吉祥'}),
               (huozhou_wantuo:Food {name: '霍州碗坨', type: '传统小吃', price_range: '低', description: '口感爽滑，酸辣开胃'}),
               (zhoushu_hotel:Accommodation {name: '霍州州署宾馆', type: '三星级酒店', price_range: '中低', rating: 4.3}),
               (meidian_hotel:Accommodation {name: '霍州煤电大酒店', type: '商务酒店', price_range: '中低', rating: 4.2}),
               (hz_bus:Transportation {name: '霍州公交', type: '公交', route: '覆盖市区', price: '1-2元'}),
               (hz_railway:Transportation {name: '霍州站', type: '火车站', route: '通往临汾等地', price: '根据里程'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '霍州'})
               WHERE a.name IN ['霍州署', '七里峪']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '霍州'}), (f:Food)
               WHERE f.name IN ['霍州年馍', '霍州碗坨']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '霍州署'}), (f:Food {name: '霍州年馍'})
               CREATE (a)-[:NEAR_FOOD {distance: '1km', tip: '署衙周边店铺可品尝特色年馍'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '霍州署'}), (f:Food {name: '霍州碗坨'})
               CREATE (a)-[:NEAR_FOOD {distance: '1.5km', tip: '市区小吃摊可体验传统碗坨'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '七里峪'}), (f:Food {name: '霍州年馍'})
               CREATE (a)-[:NEAR_FOOD {distance: '25km', tip: '返回市区后推荐购买正宗年馍'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '霍州署'}), (ac:Accommodation {name: '霍州州署宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '800m', tip: '毗邻霍州署，方便官署文化体验'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '七里峪'}), (ac:Accommodation {name: '霍州煤电大酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '23km', tip: '适合山林游览后休整'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '霍州'}), (t:Transportation)
               WHERE t.name IN ['霍州公交', '霍州站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '霍州公交'}), (t2:Transportation {name: '霍州站'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '公交直达火车站，方便前往临汾、太原等地'}]->(t2)
           """)

        print("霍州旅游数据导入完成！")

    def import_xiaoyi_data(self):
        """导入孝义旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (xy:City {name: '孝义', level: '县级市', description: '山西省县级市，吕梁代管，中国孝文化发源地'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (xiaoyi_xiaowenhua:Attraction {name: '孝义孝文化园', type: '人文景观', rating: 4.5, opening_hours: '8:30 - 17:00'}),
               (shengxihu:Attraction {name: '胜溪湖森林公园', type: '自然景观', rating: 4.4, opening_hours: '全天开放'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (xiaoyi_huoshao:Food {name: '孝义火烧', type: '地方小吃', price_range: '低', description: '外酥里嫩，馅料丰富'}),
               (xiaoyi_doufunao:Food {name: '孝义豆腐脑', type: '传统小吃', price_range: '低', description: '口感细腻，卤汁鲜美'}),
               (dongxing_hotel:Accommodation {name: '孝义东兴酒店', type: '三星级酒店', price_range: '中低', rating: 4.3}),
               (xiaoyi_hotel:Accommodation {name: '孝义宾馆', type: '商务酒店', price_range: '中低', rating: 4.2}),
               (xy_bus:Transportation {name: '孝义公交', type: '公交', route: '覆盖市区', price: '1-2元'}),
               (xy_railway:Transportation {name: '孝义站', type: '火车站', route: '通往太原等地', price: '根据里程'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '孝义'})
               WHERE a.name IN ['孝义孝文化园', '胜溪湖森林公园']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '孝义'}), (f:Food)
               WHERE f.name IN ['孝义火烧', '孝义豆腐脑']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '孝义孝文化园'}), (f:Food {name: '孝义火烧'})
               CREATE (a)-[:NEAR_FOOD {distance: '1km', tip: '文化园周边小吃店可品尝特色火烧'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '孝义孝文化园'}), (f:Food {name: '孝义豆腐脑'})
               CREATE (a)-[:NEAR_FOOD {distance: '1.2km', tip: '园区附近早餐铺可体验传统豆腐脑'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '胜溪湖森林公园'}), (f:Food {name: '孝义火烧'})
               CREATE (a)-[:NEAR_FOOD {distance: '3km', tip: '公园出口处餐馆可购买热乎火烧'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '孝义孝文化园'}), (ac:Accommodation {name: '孝义东兴酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '2km', tip: '呼应孝文化主题，适合文化研学住宿'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '胜溪湖森林公园'}), (ac:Accommodation {name: '孝义宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '4km', tip: '靠近自然景区，休闲便利'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '孝义'}), (t:Transportation)
               WHERE t.name IN ['孝义公交', '孝义站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '孝义公交'}), (t2:Transportation {name: '孝义站'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '公交直达火车站，方便前往太原、吕梁等地'}]->(t2)
           """)

        print("孝义旅游数据导入完成！")

    def import_fenyang_data(self):
        """导入汾阳旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (fy:City {name: '汾阳', level: '县级市', description: '山西省县级市，吕梁代管，中国酒都，汾酒之乡'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (fenjiu_jingqu:Attraction {name: '汾酒文化景区', type: '人文景观', rating: 4.6, opening_hours: '8:30 - 17:00'}),
               (wenfengta:Attraction {name: '文峰塔', type: '人文景观', rating: 4.4, opening_hours: '8:00 - 17:30'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (xinghuacun_fenjiu:Food {name: '汾阳杏花村汾酒', type: '地方特产', price_range: '中高', description: '清香纯正，回味悠长'}),
               (fenyang_wantu:Food {name: '汾阳碗秃', type: '传统小吃', price_range: '低', description: '口感爽滑，酸辣可口'}),
               (fenyang_international:Accommodation {name: '汾阳国际大酒店', type: '四星级酒店', price_range: '中', rating: 4.4}),
               (xinghuacun_binguan:Accommodation {name: '汾阳杏花村宾馆', type: '商务酒店', price_range: '中低', rating: 4.2}),
               (fy_bus:Transportation {name: '汾阳公交', type: '公交', route: '覆盖市区', price: '1-2元'}),
               (fy_railway:Transportation {name: '汾阳站', type: '火车站', route: '通往太原等地', price: '根据里程'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '汾阳'})
               WHERE a.name IN ['汾酒文化景区', '文峰塔']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '汾阳'}), (f:Food)
               WHERE f.name IN ['汾阳杏花村汾酒', '汾阳碗秃']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '汾酒文化景区'}), (f:Food {name: '汾阳杏花村汾酒'})
               CREATE (a)-[:NEAR_FOOD {distance: '500m', tip: '景区内可品尝原浆汾酒及购买特产'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '汾酒文化景区'}), (f:Food {name: '汾阳碗秃'})
               CREATE (a)-[:NEAR_FOOD {distance: '1km', tip: '景区周边餐馆可搭配碗秃品尝汾酒'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '文峰塔'}), (f:Food {name: '汾阳碗秃'})
               CREATE (a)-[:NEAR_FOOD {distance: '2km', tip: '塔下美食街可体验传统碗秃'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '汾酒文化景区'}), (ac:Accommodation {name: '汾阳杏花村宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '3km', tip: '毗邻酒文化景区，适合品酒体验'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '文峰塔'}), (ac:Accommodation {name: '汾阳国际大酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '1.5km', tip: '位于市区，方便文化游览后休整'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '汾阳'}), (t:Transportation)
               WHERE t.name IN ['汾阳公交', '汾阳站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '汾阳公交'}), (t2:Transportation {name: '汾阳站'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '公交直达火车站，方便前往太原、吕梁等地'}]->(t2)
           """)

        print("汾阳旅游数据导入完成！")

    def import_huhehaote_data(self):
        """导入呼和浩特旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (hhht:City {name: '呼和浩特', level: '地级市', description: '内蒙古自治区首府，中国乳都，草原明珠'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (dazhao:Attraction {name: '大召寺', type: '人文景观', rating: 4.6, opening_hours: '8:00 - 18:00'}),
               (neimenggu_museum:Attraction {name: '内蒙古博物院', type: '人文景观', rating: 4.7, opening_hours: '9:00 - 17:00'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (shoubariu:Food {name: '手把肉', type: '蒙餐', price_range: '中', description: '原汁原味，肉质鲜嫩'}),
               (naicha:Food {name: '奶茶', type: '传统饮品', price_range: '低', description: '咸香浓郁，营养丰富'}),
               (xianggelila:Accommodation {name: '呼和浩特香格里拉大酒店', type: '五星级酒店', price_range: '高', rating: 4.7}),
               (neimenggu_fandian:Accommodation {name: '内蒙古饭店', type: '五星级酒店', price_range: '高', rating: 4.6}),
               (hhht_metro1:Transportation {name: '呼和浩特地铁1号线', type: '地铁', route: '伊利健康谷-坝堰村', price: '2-6元'}),
               (baita_bus:Transportation {name: '白塔机场大巴', type: '机场巴士', route: '市区-白塔机场', price: '15-20元'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '呼和浩特'})
               WHERE a.name IN ['大召寺', '内蒙古博物院']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '呼和浩特'}), (f:Food)
               WHERE f.name IN ['手把肉', '奶茶']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '大召寺'}), (f:Food {name: '手把肉'})
               CREATE (a)-[:NEAR_FOOD {distance: '800m', tip: '寺外蒙餐馆可品尝正宗手把肉'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '大召寺'}), (f:Food {name: '奶茶'})
               CREATE (a)-[:NEAR_FOOD {distance: '500m', tip: '周边茶馆可体验传统咸奶茶'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '内蒙古博物院'}), (f:Food {name: '手把肉'})
               CREATE (a)-[:NEAR_FOOD {distance: '3km', tip: '博物院附近商圈有特色蒙餐店'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '大召寺'}), (ac:Accommodation {name: '内蒙古饭店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '1.5km', tip: '融合民族特色，方便文化体验'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '内蒙古博物院'}), (ac:Accommodation {name: '呼和浩特香格里拉大酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '2km', tip: '毗邻文化地标，适合商务休闲'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '呼和浩特'}), (t:Transportation)
               WHERE t.name IN ['呼和浩特地铁1号线', '白塔机场大巴']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '呼和浩特地铁1号线'}), (t2:Transportation {name: '白塔机场大巴'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '地铁可至机场大巴停靠点，便捷前往白塔机场'}]->(t2)
           """)

        print("呼和浩特旅游数据导入完成！")

    def import_baotou_data(self):
        """导入包头旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (bt:City {name: '包头', level: '地级市', description: '内蒙古自治区重要工业城市，草原钢城，稀土之都'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (wudangzhao:Attraction {name: '五当召', type: '人文景观', rating: 4.6, opening_hours: '8:30 - 17:00'}),
               (saihantala:Attraction {name: '赛汗塔拉草原', type: '自然景观', rating: 4.7, opening_hours: '全天开放'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (baotou_kaoyangtui:Food {name: '包头烤羊腿', type: '蒙餐', price_range: '中高', description: '外焦里嫩，香味浓郁'}),
               (youmian:Food {name: '莜面', type: '地方主食', price_range: '低', description: '口感劲道，健康营养'}),
               (bt_xianggelila:Accommodation {name: '包头香格里拉大酒店', type: '五星级酒店', price_range: '高', rating: 4.6}),
               (baotou_binguan:Accommodation {name: '包头宾馆', type: '四星级酒店', price_range: '中', rating: 4.4}),
               (bt_bus:Transportation {name: '包头公交', type: '公交', route: '覆盖市区', price: '1-2元'}),
               (bt_railway:Transportation {name: '包头站', type: '火车站', route: '通往呼和浩特等地', price: '根据里程'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '包头'})
               WHERE a.name IN ['五当召', '赛汗塔拉草原']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '包头'}), (f:Food)
               WHERE f.name IN ['包头烤羊腿', '莜面']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '赛汗塔拉草原'}), (f:Food {name: '包头烤羊腿'})
               CREATE (a)-[:NEAR_FOOD {distance: '1km', tip: '草原景区内可体验现烤羊腿'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '赛汗塔拉草原'}), (f:Food {name: '莜面'})
               CREATE (a)-[:NEAR_FOOD {distance: '2km', tip: '景区周边餐馆可品尝多种莜面做法'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '五当召'}), (f:Food {name: '莜面'})
               CREATE (a)-[:NEAR_FOOD {distance: '10km', tip: '召庙附近农家可体验传统莜面主食'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '五当召'}), (ac:Accommodation {name: '包头宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '50km', tip: '返回市区后便捷休整，性价比高'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '赛汗塔拉草原'}), (ac:Accommodation {name: '包头香格里拉大酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '3km', tip: '毗邻草原景区，适合休闲度假'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '包头'}), (t:Transportation)
               WHERE t.name IN ['包头公交', '包头站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '包头公交'}), (t2:Transportation {name: '包头站'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '公交直达火车站，方便前往呼和浩特、鄂尔多斯等地'}]->(t2)
           """)

        print("包头旅游数据导入完成！")

    def import_wuhai_data(self):
        """导入乌海旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (wh:City {name: '乌海', level: '地级市', description: '内蒙古自治区地级市，黄河明珠，书法之城'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (jinshawan:Attraction {name: '金沙湾', type: '自然景观', rating: 4.4, opening_hours: '8:00 - 18:00'}),
               (gandeershan:Attraction {name: '甘德尔山', type: '自然景观', rating: 4.3, opening_hours: '8:30 - 17:30'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (wuhai_putao:Food {name: '乌海葡萄', type: '地方特产', price_range: '低', description: '甜度高，汁多味美'}),
               (wuhai_huangheliyu:Food {name: '黄河鲤鱼', type: '地方特色', price_range: '中', description: '肉质鲜嫩，营养丰富'}),
               (wuhai_binguan:Accommodation {name: '乌海宾馆', type: '四星级酒店', price_range: '中', rating: 4.4}),
               (lantian_dajiudian:Accommodation {name: '乌海蓝天大酒店', type: '商务酒店', price_range: '中低', rating: 4.2}),
               (wh_bus:Transportation {name: '乌海公交', type: '公交', route: '覆盖市区', price: '1-2元'}),
               (wh_railway:Transportation {name: '乌海站', type: '火车站', route: '通往包头等地', price: '根据里程'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '乌海'})
               WHERE a.name IN ['金沙湾', '甘德尔山']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '乌海'}), (f:Food)
               WHERE f.name IN ['乌海葡萄', '黄河鲤鱼']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '金沙湾'}), (f:Food {name: '乌海葡萄'})
               CREATE (a)-[:NEAR_FOOD {distance: '5km', tip: '景区特产店可购买新鲜葡萄及葡萄酒'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '金沙湾'}), (f:Food {name: '黄河鲤鱼'})
               CREATE (a)-[:NEAR_FOOD {distance: '8km', tip: '临近黄河沿岸餐馆可品尝正宗鲤鱼'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '甘德尔山'}), (f:Food {name: '乌海葡萄'})
               CREATE (a)-[:NEAR_FOOD {distance: '12km', tip: '下山后市区水果店可购买优质葡萄'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '金沙湾'}), (ac:Accommodation {name: '乌海宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '15km', tip: '适合沙漠游玩后舒适休整'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '甘德尔山'}), (ac:Accommodation {name: '乌海蓝天大酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '10km', tip: '靠近景区，性价比高'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '乌海'}), (t:Transportation)
               WHERE t.name IN ['乌海公交', '乌海站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '乌海公交'}), (t2:Transportation {name: '乌海站'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '公交直达火车站，方便前往包头、银川等地'}]->(t2)
           """)

        print("乌海旅游数据导入完成！")

    def import_chifeng_data(self):
        """导入赤峰旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (cf:City {name: '赤峰', level: '地级市', description: '内蒙古自治区地级市，红山文化发祥地，草原青铜器之都'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (kesikten_shizhen:Attraction {name: '克什克腾石阵', type: '自然景观', rating: 4.7, opening_hours: '8:00 - 17:30'}),
               (wulanbutong:Attraction {name: '乌兰布统草原', type: '自然景观', rating: 4.6, opening_hours: '全天开放'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (chifeng_duijia:Food {name: '赤峰对夹', type: '地方特色', price_range: '低', description: '外酥里嫩，肉香浓郁'}),
               (chifeng_shoubariu:Food {name: '手把肉', type: '蒙餐', price_range: '中', description: '原汁原味，鲜嫩可口'}),
               (wanda_jiahua:Accommodation {name: '赤峰万达嘉华酒店', type: '五星级酒店', price_range: '高', rating: 4.6}),
               (chifeng_binguan:Accommodation {name: '赤峰宾馆', type: '四星级酒店', price_range: '中', rating: 4.4}),
               (cf_bus:Transportation {name: '赤峰公交', type: '公交', route: '覆盖市区', price: '1-2元'}),
               (cf_railway:Transportation {name: '赤峰站', type: '火车站', route: '通往北京等地', price: '根据里程'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '赤峰'})
               WHERE a.name IN ['克什克腾石阵', '乌兰布统草原']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '赤峰'}), (f:Food)
               WHERE f.name IN ['赤峰对夹', '手把肉']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '乌兰布统草原'}), (f:Food {name: '手把肉'})
               CREATE (a)-[:NEAR_FOOD {distance: '1km', tip: '草原度假村可体验现煮手把肉'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '乌兰布统草原'}), (f:Food {name: '赤峰对夹'})
               CREATE (a)-[:NEAR_FOOD {distance: '3km', tip: '景区服务区可购买特色对夹'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '克什克腾石阵'}), (f:Food {name: '赤峰对夹'})
               CREATE (a)-[:NEAR_FOOD {distance: '20km', tip: '景区出口小镇可品尝热乎对夹'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '克什克腾石阵'}), (ac:Accommodation {name: '赤峰宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '150km', tip: '适合长途游览后市区休整'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '乌兰布统草原'}), (ac:Accommodation {name: '赤峰万达嘉华酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '120km', tip: '返回市区后享受高品质住宿'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '赤峰'}), (t:Transportation)
               WHERE t.name IN ['赤峰公交', '赤峰站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '赤峰公交'}), (t2:Transportation {name: '赤峰站'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '公交直达火车站，方便前往北京、通辽等地'}]->(t2)
           """)

        print("赤峰旅游数据导入完成！")

    def import_tongliao_data(self):
        """导入通辽旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (tl:City {name: '通辽', level: '地级市', description: '内蒙古自治区地级市，科尔沁草原核心区域'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (daqinggou:Attraction {name: '大青沟', type: '自然景观', rating: 4.6, opening_hours: '8:00 - 17:30'}),
               (xiaozhuangyuan:Attraction {name: '孝庄园文化旅游区', type: '人文景观', rating: 4.5, opening_hours: '8:30 - 17:00'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (tongliao_niurougan:Food {name: '通辽牛肉干', type: '地方特产', price_range: '中', description: '肉质紧实，风味独特'}),
               (chaomi:Food {name: '炒米', type: '传统美食', price_range: '低', description: '香脆可口，奶香浓郁'}),
               (tongliao_hilton:Accommodation {name: '通辽希尔顿酒店', type: '五星级酒店', price_range: '高', rating: 4.6}),
               (tongliao_binguan:Accommodation {name: '通辽宾馆', type: '四星级酒店', price_range: '中', rating: 4.4}),
               (tl_bus:Transportation {name: '通辽公交', type: '公交', route: '覆盖市区', price: '1-2元'}),
               (tl_railway:Transportation {name: '通辽站', type: '火车站', route: '通往沈阳等地', price: '根据里程'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '通辽'})
               WHERE a.name IN ['大青沟', '孝庄园文化旅游区']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '通辽'}), (f:Food)
               WHERE f.name IN ['通辽牛肉干', '炒米']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '孝庄园文化旅游区'}), (f:Food {name: '通辽牛肉干'})
               CREATE (a)-[:NEAR_FOOD {distance: '2km', tip: '景区特产店可购买正宗牛肉干'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '孝庄园文化旅游区'}), (f:Food {name: '炒米'})
               CREATE (a)-[:NEAR_FOOD {distance: '1.5km', tip: '园区蒙古包可体验传统炒米配奶茶'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '大青沟'}), (f:Food {name: '通辽牛肉干'})
               CREATE (a)-[:NEAR_FOOD {distance: '30km', tip: '景区出口商店可选购特色牛肉干'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '大青沟'}), (ac:Accommodation {name: '通辽宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '100km', tip: '适合自然探索后市区休整'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '孝庄园文化旅游区'}), (ac:Accommodation {name: '通辽希尔顿酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '40km', tip: '返回市区后享受高品质服务'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '通辽'}), (t:Transportation)
               WHERE t.name IN ['通辽公交', '通辽站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '通辽公交'}), (t2:Transportation {name: '通辽站'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '公交直达火车站，方便前往沈阳、赤峰等地'}]->(t2)
           """)

        print("通辽旅游数据导入完成！")

    def import_eerduosi_data(self):
        """导入鄂尔多斯旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (eeds:City {name: '鄂尔多斯', level: '地级市', description: '内蒙古自治区地级市，中国绒城，能源重化工基地'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (xiangsawan:Attraction {name: '响沙湾', type: '自然景观', rating: 4.7, opening_hours: '8:00 - 18:00'}),
               (chengjisihanling:Attraction {name: '成吉思汗陵', type: '人文景观', rating: 4.6, opening_hours: '8:30 - 17:30'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (eeds_shoubariu:Food {name: '鄂尔多斯手把肉', type: '蒙餐', price_range: '中', description: '肉质鲜嫩，原汁原味'}),
               (nailao:Food {name: '奶酪', type: '奶制品', price_range: '低', description: '奶香浓郁，营养丰富'}),
               (eeds_crowne:Accommodation {name: '鄂尔多斯皇冠假日酒店', type: '五星级酒店', price_range: '高', rating: 4.7}),
               (eeds_binguan:Accommodation {name: '鄂尔多斯宾馆', type: '四星级酒店', price_range: '中', rating: 4.5}),
               (eeds_bus:Transportation {name: '鄂尔多斯公交', type: '公交', route: '覆盖市区', price: '1-2元'}),
               (eeds_railway:Transportation {name: '鄂尔多斯站', type: '火车站', route: '通往呼和浩特等地', price: '根据里程'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '鄂尔多斯'})
               WHERE a.name IN ['响沙湾', '成吉思汗陵']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '鄂尔多斯'}), (f:Food)
               WHERE f.name IN ['鄂尔多斯手把肉', '奶酪']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '响沙湾'}), (f:Food {name: '鄂尔多斯手把肉'})
               CREATE (a)-[:NEAR_FOOD {distance: '2km', tip: '沙漠度假村可体验现煮手把肉'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '响沙湾'}), (f:Food {name: '奶酪'})
               CREATE (a)-[:NEAR_FOOD {distance: '1.5km', tip: '景区商店可购买多种风味奶酪'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '成吉思汗陵'}), (f:Food {name: '鄂尔多斯手把肉'})
               CREATE (a)-[:NEAR_FOOD {distance: '5km', tip: '陵寝周边蒙古包餐馆可品尝特色手把肉'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '响沙湾'}), (ac:Accommodation {name: '鄂尔多斯皇冠假日酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '50km', tip: '适合沙漠游玩后高品质休整'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '成吉思汗陵'}), (ac:Accommodation {name: '鄂尔多斯宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '30km', tip: '靠近文化景区，方便深度游览'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '鄂尔多斯'}), (t:Transportation)
               WHERE t.name IN ['鄂尔多斯公交', '鄂尔多斯站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '鄂尔多斯公交'}), (t2:Transportation {name: '鄂尔多斯站'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '公交直达火车站，方便前往呼和浩特、包头等地'}]->(t2)
           """)

        print("鄂尔多斯旅游数据导入完成！")

    def import_bayannur_data(self):
        """导入巴彦淖尔旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (byne:City {name: '巴彦淖尔', level: '地级市', description: '内蒙古自治区地级市，塞上粮仓，黄河几字湾顶端'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (nalinhu:Attraction {name: '纳林湖', type: '自然景观', rating: 4.5, opening_hours: '8:00 - 18:00'}),
               (hetao_wenhua:Attraction {name: '黄河河套文化旅游区', type: '人文景观', rating: 4.4, opening_hours: '8:30 - 17:30'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (hetao_ying sipan:Food {name: '河套硬四盘', type: '地方特色', price_range: '中', description: '传统宴席，风味独特'}),
               (bynr_hualaishi:Food {name: '巴彦淖尔华莱士瓜', type: '地方特产', price_range: '低', description: '香甜多汁，品质优良'}),
               (bayannur_fandian:Accommodation {name: '巴彦淖尔饭店', type: '四星级酒店', price_range: '中', rating: 4.4}),
               (bayannur_huawei:Accommodation {name: '巴彦淖尔华威大酒店', type: '商务酒店', price_range: '中低', rating: 4.2}),
               (byne_bus:Transportation {name: '巴彦淖尔公交', type: '公交', route: '覆盖市区', price: '1-2元'}),
               (linhe_railway:Transportation {name: '临河站', type: '火车站', route: '通往呼和浩特等地', price: '根据里程'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '巴彦淖尔'})
               WHERE a.name IN ['纳林湖', '黄河河套文化旅游区']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '巴彦淖尔'}), (f:Food)
               WHERE f.name IN ['河套硬四盘', '巴彦淖尔华莱士瓜']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '黄河河套文化旅游区'}), (f:Food {name: '河套硬四盘'})
               CREATE (a)-[:NEAR_FOOD {distance: '1.5km', tip: '景区民俗餐馆可品尝传统宴席'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '黄河河套文化旅游区'}), (f:Food {name: '巴彦淖尔华莱士瓜'})
               CREATE (a)-[:NEAR_FOOD {distance: '2km', tip: '景区特产区可购买新鲜华莱士瓜'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '纳林湖'}), (f:Food {name: '巴彦淖尔华莱士瓜'})
               CREATE (a)-[:NEAR_FOOD {distance: '30km', tip: '湖区周边瓜田可体验采摘乐趣'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '纳林湖'}), (ac:Accommodation {name: '巴彦淖尔华威大酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '40km', tip: '适合湖区游览后经济休整'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '黄河河套文化旅游区'}), (ac:Accommodation {name: '巴彦淖尔饭店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '3km', tip: '毗邻文化景区，方便深度体验'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '巴彦淖尔'}), (t:Transportation)
               WHERE t.name IN ['巴彦淖尔公交', '临河站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '巴彦淖尔公交'}), (t2:Transportation {name: '临河站'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '公交直达火车站，方便前往呼和浩特、银川等地'}]->(t2)
           """)

        print("巴彦淖尔旅游数据导入完成！")

    def import_wulanchabu_data(self):
        """导入乌兰察布旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (wlcbs:City {name: '乌兰察布', level: '地级市', description: '内蒙古自治区地级市，中国草原避暑之都，风电之都'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (huitengxile:Attraction {name: '辉腾锡勒草原', type: '自然景观', rating: 4.6, opening_hours: '全天开放'}),
               (huoshan_dizhi:Attraction {name: '火山地质公园', type: '自然景观', rating: 4.5, opening_hours: '8:00 - 17:30'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (wlcbs_nailao:Food {name: '乌兰察布奶酪', type: '奶制品', price_range: '低', description: '奶香浓郁，口感细腻'}),
               (wlcbs_shoubariu:Food {name: '手把肉', type: '蒙餐', price_range: '中', description: '肉质鲜嫩，原汁原味'}),
               (duomengde:Accommodation {name: '乌兰察布多蒙德豪生大酒店', type: '五星级酒店', price_range: '高', rating: 4.5}),
               (wlcbs_binguan:Accommodation {name: '乌兰察布宾馆', type: '四星级酒店', price_range: '中', rating: 4.3}),
               (wlcbs_bus:Transportation {name: '乌兰察布公交', type: '公交', route: '覆盖市区', price: '1-2元'}),
               (wlcbs_highspeed:Transportation {name: '乌兰察布站', type: '高铁站', route: '通往北京等地', price: '根据里程'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '乌兰察布'})
               WHERE a.name IN ['辉腾锡勒草原', '火山地质公园']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '乌兰察布'}), (f:Food)
               WHERE f.name IN ['乌兰察布奶酪', '手把肉']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '辉腾锡勒草原'}), (f:Food {name: '乌兰察布奶酪'})
               CREATE (a)-[:NEAR_FOOD {distance: '1km', tip: '草原蒙古包可品尝现制奶制品'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '辉腾锡勒草原'}), (f:Food {name: '手把肉'})
               CREATE (a)-[:NEAR_FOOD {distance: '1.5km', tip: '草原度假村可体验正宗手把肉'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '火山地质公园'}), (f:Food {name: '乌兰察布奶酪'})
               CREATE (a)-[:NEAR_FOOD {distance: '20km', tip: '景区服务区可购买特色奶酪'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '辉腾锡勒草原'}), (ac:Accommodation {name: '乌兰察布多蒙德豪生大酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '60km', tip: '适合草原避暑后高品质休整'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '火山地质公园'}), (ac:Accommodation {name: '乌兰察布宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '30km', tip: '靠近景区，方便地质探秘行程'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '乌兰察布'}), (t:Transportation)
               WHERE t.name IN ['乌兰察布公交', '乌兰察布站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '乌兰察布公交'}), (t2:Transportation {name: '乌兰察布站'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '公交直达高铁站，快速连接北京、呼和浩特等地'}]->(t2)
           """)

        print("乌兰察布旅游数据导入完成！")

    def import_huolinguole_data(self):
        """导入霍林郭勒旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (hlgl:City {name: '霍林郭勒', level: '县级市', description: '内蒙古自治区县级市，通辽代管，草原煤城'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (kehanshan:Attraction {name: '可汗山', type: '人文景观', rating: 4.4, opening_hours: '8:00 - 17:30'}),
               (guanyinshan:Attraction {name: '观音山', type: '自然景观', rating: 4.3, opening_hours: '全天开放'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (hlgl_kaoyangpai:Food {name: '霍林郭勒烤羊排', type: '地方特色', price_range: '中', description: '外焦里嫩，香味浓郁'}),
               (naidoufu:Food {name: '奶豆腐', type: '传统奶食', price_range: '低', description: '酸甜可口，营养丰富'}),
               (huolinguole_binguan:Accommodation {name: '霍林郭勒宾馆', type: '三星级酒店', price_range: '中低', rating: 4.3}),
               (huomei_binguan:Accommodation {name: '霍煤宾馆', type: '商务酒店', price_range: '中低', rating: 4.2}),
               (hlgl_bus:Transportation {name: '霍林郭勒公交', type: '公交', route: '覆盖市区', price: '1-2元'}),
               (hlgl_railway:Transportation {name: '霍林郭勒站', type: '火车站', route: '通往通辽等地', price: '根据里程'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '霍林郭勒'})
               WHERE a.name IN ['可汗山', '观音山']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '霍林郭勒'}), (f:Food)
               WHERE f.name IN ['霍林郭勒烤羊排', '奶豆腐']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '可汗山'}), (f:Food {name: '霍林郭勒烤羊排'})
               CREATE (a)-[:NEAR_FOOD {distance: '2km', tip: '山脚下蒙古包餐馆可品尝现烤羊排'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '可汗山'}), (f:Food {name: '奶豆腐'})
               CREATE (a)-[:NEAR_FOOD {distance: '1.5km', tip: '景区特产店可购买手工奶豆腐'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '观音山'}), (f:Food {name: '霍林郭勒烤羊排'})
               CREATE (a)-[:NEAR_FOOD {distance: '5km', tip: '下山后镇上餐馆可体验特色烤羊排'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '可汗山'}), (ac:Accommodation {name: '霍林郭勒宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '8km', tip: '适合文化游览后舒适休整'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '观音山'}), (ac:Accommodation {name: '霍煤宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '10km', tip: '靠近景区，性价比高'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '霍林郭勒'}), (t:Transportation)
               WHERE t.name IN ['霍林郭勒公交', '霍林郭勒站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '霍林郭勒公交'}), (t2:Transportation {name: '霍林郭勒站'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '公交直达火车站，方便前往通辽、沈阳等地'}]->(t2)
           """)

        print("霍林郭勒旅游数据导入完成！")

    def import_manzhouli_data(self):
        """导入满洲里旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (mzl:City {name: '满洲里', level: '县级市', description: '内蒙古自治区县级市，呼伦贝尔代管，东亚之窗，口岸名城'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (guomen_jingqu:Attraction {name: '国门景区', type: '人文景观', rating: 4.7, opening_hours: '8:30 - 17:30'}),
               (taowa_guangchang:Attraction {name: '套娃广场', type: '人文景观', rating: 4.6, opening_hours: '全天开放'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (eshi_xican:Food {name: '俄式西餐', type: '异国风味', price_range: '中', description: '风味独特，异域情调'}),
               (mzl_kaoyangtui:Food {name: '烤羊腿', type: '蒙餐', price_range: '中高', description: '外焦里嫩，肉质鲜美'}),
               (taowa_jiudian:Accommodation {name: '满洲里套娃酒店', type: '特色酒店', price_range: '中高', rating: 4.6}),
               (manzhouli_fandian:Accommodation {name: '满洲里饭店', type: '四星级酒店', price_range: '中', rating: 4.4}),
               (mzl_bus:Transportation {name: '满洲里公交', type: '公交', route: '覆盖市区', price: '1-2元'}),
               (mzl_railway:Transportation {name: '满洲里站', type: '火车站', route: '通往哈尔滨等地', price: '根据里程'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '满洲里'})
               WHERE a.name IN ['国门景区', '套娃广场']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '满洲里'}), (f:Food)
               WHERE f.name IN ['俄式西餐', '烤羊腿']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '套娃广场'}), (f:Food {name: '俄式西餐'})
               CREATE (a)-[:NEAR_FOOD {distance: '500m', tip: '广场内俄式餐厅可体验异国风味'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '套娃广场'}), (f:Food {name: '烤羊腿'})
               CREATE (a)-[:NEAR_FOOD {distance: '1km', tip: '周边蒙餐馆可品尝特色烤羊腿'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '国门景区'}), (f:Food {name: '俄式西餐'})
               CREATE (a)-[:NEAR_FOOD {distance: '3km', tip: '景区返程沿途有俄式风味餐馆'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '国门景区'}), (ac:Accommodation {name: '满洲里饭店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '5km', tip: '适合口岸文化游览后休整'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '套娃广场'}), (ac:Accommodation {name: '满洲里套娃酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '800m', tip: '与广场主题呼应，沉浸式体验三国文化'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '满洲里'}), (t:Transportation)
               WHERE t.name IN ['满洲里公交', '满洲里站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '满洲里公交'}), (t2:Transportation {name: '满洲里站'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '公交直达火车站，方便前往哈尔滨、呼伦贝尔等地'}]->(t2)
           """)

        print("满洲里旅游数据导入完成！")

    def import_yakeshi_data(self):
        """导入牙克石旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (yks:City {name: '牙克石', level: '县级市', description: '内蒙古自治区县级市，呼伦贝尔代管，中国森林工业之城'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (fenghuangshan:Attraction {name: '凤凰山滑雪场', type: '运动休闲', rating: 4.5, opening_hours: '9:00 - 16:30'}),
               (chuoerhe:Attraction {name: '绰尔河峡谷', type: '自然景观', rating: 4.4, opening_hours: '全天开放'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (yks_kaolengmian:Food {name: '牙克石烤冷面', type: '地方小吃', price_range: '低', description: '酸甜可口，风味独特'}),
               (yesheng_mogu:Food {name: '野生蘑菇', type: '山珍特产', price_range: '中', description: '味道鲜美，营养丰富'}),
               (yakeshi_binguan:Accommodation {name: '牙克石宾馆', type: '三星级酒店', price_range: '中低', rating: 4.3}),
               (linye_binguan:Accommodation {name: '牙克石林业宾馆', type: '商务酒店', price_range: '中低', rating: 4.2}),
               (yks_bus:Transportation {name: '牙克石公交', type: '公交', route: '覆盖市区', price: '1-2元'}),
               (yks_railway:Transportation {name: '牙克石站', type: '火车站', route: '通往海拉尔等地', price: '根据里程'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '牙克石'})
               WHERE a.name IN ['凤凰山滑雪场', '绰尔河峡谷']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '牙克石'}), (f:Food)
               WHERE f.name IN ['牙克石烤冷面', '野生蘑菇']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '凤凰山滑雪场'}), (f:Food {name: '牙克石烤冷面'})
               CREATE (a)-[:NEAR_FOOD {distance: '1km', tip: '滑雪场服务区可品尝热乎烤冷面'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '凤凰山滑雪场'}), (f:Food {name: '野生蘑菇'})
               CREATE (a)-[:NEAR_FOOD {distance: '5km', tip: '附近餐馆有用野生蘑菇做的热汤'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '绰尔河峡谷'}), (f:Food {name: '野生蘑菇'})
               CREATE (a)-[:NEAR_FOOD {distance: '3km', tip: '峡谷周边可购买新鲜山采蘑菇'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '凤凰山滑雪场'}), (ac:Accommodation {name: '牙克石宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '15km', tip: '适合冰雪运动后舒适休整'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '绰尔河峡谷'}), (ac:Accommodation {name: '牙克石林业宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '20km', tip: '靠近林区，方便峡谷探秘'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '牙克石'}), (t:Transportation)
               WHERE t.name IN ['牙克石公交', '牙克石站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '牙克石公交'}), (t2:Transportation {name: '牙克石站'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '公交直达火车站，方便前往海拉尔、满洲里等地'}]->(t2)
           """)

        print("牙克石旅游数据导入完成！")

    def import_zhalantun_data(self):
        """导入扎兰屯旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (zlt:City {name: '扎兰屯', level: '县级市', description: '内蒙古自治区县级市，呼伦贝尔代管，塞外苏杭'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (diaoqiao_gongyuan:Attraction {name: '吊桥公园', type: '人文景观', rating: 4.5, opening_hours: '全天开放'}),
               (xiushui_fengjingqu:Attraction {name: '秀水风景区', type: '自然景观', rating: 4.4, opening_hours: '8:00 - 17:30'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (zlt_shaguo:Food {name: '扎兰屯沙果', type: '地方特产', price_range: '低', description: '酸甜适中，果香浓郁'}),
               (zlt_kaoyangtui:Food {name: '烤羊腿', type: '地方特色', price_range: '中', description: '外焦里嫩，香味扑鼻'}),
               (zhalantun_binguan:Accommodation {name: '扎兰屯宾馆', type: '三星级酒店', price_range: '中低', rating: 4.3}),
               (chengjisihan_binguan:Accommodation {name: '扎兰屯成吉思汗宾馆', type: '商务酒店', price_range: '中低', rating: 4.2}),
               (zlt_bus:Transportation {name: '扎兰屯公交', type: '公交', route: '覆盖市区', price: '1-2元'}),
               (zlt_railway:Transportation {name: '扎兰屯站', type: '火车站', route: '通往齐齐哈尔等地', price: '根据里程'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '扎兰屯'})
               WHERE a.name IN ['吊桥公园', '秀水风景区']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '扎兰屯'}), (f:Food)
               WHERE f.name IN ['扎兰屯沙果', '烤羊腿']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '吊桥公园'}), (f:Food {name: '扎兰屯沙果'})
               CREATE (a)-[:NEAR_FOOD {distance: '800m', tip: '公园周边果摊可购买新鲜沙果'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '吊桥公园'}), (f:Food {name: '烤羊腿'})
               CREATE (a)-[:NEAR_FOOD {distance: '1.2km', tip: '公园附近餐馆可品尝特色烤羊腿'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '秀水风景区'}), (f:Food {name: '扎兰屯沙果'})
               CREATE (a)-[:NEAR_FOOD {distance: '5km', tip: '景区出口处有沙果干等加工特产'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '吊桥公园'}), (ac:Accommodation {name: '扎兰屯宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '2km', tip: '毗邻园林景区，方便休闲游览'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '秀水风景区'}), (ac:Accommodation {name: '扎兰屯成吉思汗宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '8km', tip: '适合自然风光游览后休整'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '扎兰屯'}), (t:Transportation)
               WHERE t.name IN ['扎兰屯公交', '扎兰屯站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '扎兰屯公交'}), (t2:Transportation {name: '扎兰屯站'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '公交直达火车站，方便前往齐齐哈尔、海拉尔等地'}]->(t2)
           """)

        print("扎兰屯旅游数据导入完成！")

    def import_eerguna_data(self):
        """导入额尔古纳旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (egn:City {name: '额尔古纳', level: '县级市', description: '内蒙古自治区县级市，呼伦贝尔代管，中俄中俄边境口岸城市'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (egn_shidi:Attraction {name: '额尔古纳湿地', type: '自然景观', rating: 4.7, opening_hours: '8:00 - 17:30'}),
               (baihualin:Attraction {name: '白桦林景区', type: '自然景观', rating: 4.5, opening_hours: '全天开放'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (lieba:Food {name: '列巴', type: '俄式美食', price_range: '中低', description: '外脆内软，麦香浓郁'}),
               (egn_shoubariu:Food {name: '手把肉', type: '蒙餐', price_range: '中', description: '原汁原味，肉质鲜嫩'}),
               (eerguna_dajiudian:Accommodation {name: '额尔古纳大酒店', type: '四星级酒店', price_range: '中', rating: 4.5}),
               (eerguna_binguan:Accommodation {name: '额尔古纳宾馆', type: '商务酒店', price_range: '中低', rating: 4.3}),
               (egn_bus:Transportation {name: '额尔古纳公交', type: '公交', route: '覆盖市区', price: '1-2元'}),
               (labudalin_railway:Transportation {name: '拉布大林站', type: '火车站', route: '通往海拉尔等地', price: '根据里程'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '额尔古纳'})
               WHERE a.name IN ['额尔古纳湿地', '白桦林景区']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '额尔古纳'}), (f:Food)
               WHERE f.name IN ['列巴', '手把肉']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '白桦林景区'}), (f:Food {name: '列巴'})
               CREATE (a)-[:NEAR_FOOD {distance: '2km', tip: '景区周边俄式木屋可品尝现烤列巴'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '白桦林景区'}), (f:Food {name: '手把肉'})
               CREATE (a)-[:NEAR_FOOD {distance: '3km', tip: '附近草原毡房可体验正宗手把肉'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '额尔古纳湿地'}), (f:Food {name: '列巴'})
               CREATE (a)-[:NEAR_FOOD {distance: '5km', tip: '景区出口小镇有俄式面包房'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '额尔古纳湿地'}), (ac:Accommodation {name: '额尔古纳大酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '8km', tip: '适合湿地游览后舒适休整'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '白桦林景区'}), (ac:Accommodation {name: '额尔古纳宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '6km', tip: '靠近林区，方便自然探秘'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '额尔古纳'}), (t:Transportation)
               WHERE t.name IN ['额尔古纳公交', '拉布大林站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '额尔古纳公交'}), (t2:Transportation {name: '拉布大林站'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '公交直达火车站，方便前往海拉尔、满洲里等地'}]->(t2)
           """)

        print("额尔古纳旅游数据导入完成！")

    def import_genhe_data(self):
        """导入根河旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (gh:City {name: '根河', level: '县级市', description: '内蒙古自治区县级市，呼伦贝尔代管，中国冷极'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (aoluguya:Attraction {name: '敖鲁古雅使鹿部落', type: '人文景观', rating: 4.6, opening_hours: '8:30 - 17:00'}),
               (lengjicun:Attraction {name: '冷极村', type: '特色村落', rating: 4.5, opening_hours: '全天开放'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (lurougan:Food {name: '鹿肉干', type: '地方特产', price_range: '中', description: '肉质紧实，营养丰富'}),
               (lanmeijiang:Food {name: '蓝莓酱', type: '地方特产', price_range: '低', description: '酸甜可口，野生风味'}),
               (genhe_binguan:Accommodation {name: '根河宾馆', type: '三星级酒店', price_range: '中低', rating: 4.3}),
               (genhe_linye:Accommodation {name: '根河林业宾馆', type: '商务酒店', price_range: '中低', rating: 4.2}),
               (gh_bus:Transportation {name: '根河公交', type: '公交', route: '覆盖市区', price: '1-2元'}),
               (gh_railway:Transportation {name: '根河站', type: '火车站', route: '通往海拉尔等地', price: '根据里程'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '根河'})
               WHERE a.name IN ['敖鲁古雅使鹿部落', '冷极村']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '根河'}), (f:Food)
               WHERE f.name IN ['鹿肉干', '蓝莓酱']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '敖鲁古雅使鹿部落'}), (f:Food {name: '鹿肉干'})
               CREATE (a)-[:NEAR_FOOD {distance: '500m', tip: '部落文化体验区可购买现制鹿肉干'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '敖鲁古雅使鹿部落'}), (f:Food {name: '蓝莓酱'})
               CREATE (a)-[:NEAR_FOOD {distance: '800m', tip: '部落商店有野生蓝莓制作的果酱'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '冷极村'}), (f:Food {name: '蓝莓酱'})
               CREATE (a)-[:NEAR_FOOD {distance: '2km', tip: '村里农家乐可用蓝莓酱搭配主食'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '敖鲁古雅使鹿部落'}), (ac:Accommodation {name: '根河宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '10km', tip: '适合驯鹿文化体验后舒适休整'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '冷极村'}), (ac:Accommodation {name: '根河林业宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '15km', tip: '靠近林区，适配冷极村探秘行程'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '根河'}), (t:Transportation)
               WHERE t.name IN ['根河公交', '根河站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '根河公交'}), (t2:Transportation {name: '根河站'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '公交直达火车站，方便前往海拉尔、额尔古纳等地'}]->(t2)
           """)

        print("根河旅游数据导入完成！")

    def import_fengzhen_data(self):
        """导入丰镇旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (fz:City {name: '丰镇', level: '县级市', description: '内蒙古自治区县级市，乌兰察布代管，月饼之乡'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (xuegangshan:Attraction {name: '薛刚山', type: '自然景观', rating: 4.3, opening_hours: '全天开放'}),
               (jinlongmiao:Attraction {name: '金龙大王庙', type: '人文景观', rating: 4.2, opening_hours: '8:30 - 17:00'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (fengzhen_yuebing:Food {name: '丰镇月饼', type: '地方特产', price_range: '低', description: '酥脆香甜，历史悠久'}),
               (fengzhen_xunji:Food {name: '丰镇熏鸡', type: '传统美食', price_range: '中低', description: '色泽红亮，熏香浓郁'}),
               (fengzhen_binguan:Accommodation {name: '丰镇宾馆', type: '三星级酒店', price_range: '中低', rating: 4.2}),
               (fengzhen_yingbin:Accommodation {name: '丰镇迎宾酒店', type: '商务酒店', price_range: '中低', rating: 4.1}),
               (fz_bus:Transportation {name: '丰镇公交', type: '公交', route: '覆盖市区', price: '1-2元'}),
               (fz_railway:Transportation {name: '丰镇站', type: '火车站', route: '通往集宁等地', price: '根据里程'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '丰镇'})
               WHERE a.name IN ['薛刚山', '金龙大王庙']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '丰镇'}), (f:Food)
               WHERE f.name IN ['丰镇月饼', '丰镇熏鸡']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '薛刚山'}), (f:Food {name: '丰镇月饼'})
               CREATE (a)-[:NEAR_FOOD {distance: '1km', tip: '山脚特产店可购买现做月饼'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '薛刚山'}), (f:Food {name: '丰镇熏鸡'})
               CREATE (a)-[:NEAR_FOOD {distance: '1.5km', tip: '下山后老街餐馆可品尝正宗熏鸡'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '金龙大王庙'}), (f:Food {name: '丰镇月饼'})
               CREATE (a)-[:NEAR_FOOD {distance: '800m', tip: '庙外市集有传统工艺月饼售卖'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '薛刚山'}), (ac:Accommodation {name: '丰镇宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '3km', tip: '适合登山游览后休整，可品尝酒店月饼礼盒'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '金龙大王庙'}), (ac:Accommodation {name: '丰镇迎宾酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '2km', tip: '毗邻人文景区，方便文化探访'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '丰镇'}), (t:Transportation)
               WHERE t.name IN ['丰镇公交', '丰镇站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '丰镇公交'}), (t2:Transportation {name: '丰镇站'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '公交直达火车站，方便前往集宁、大同等地'}]->(t2)
           """)

        print("丰镇旅游数据导入完成！")

    def import_wulanhaote_data(self):
        """导入乌兰浩特旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (wlht:City {name: '乌兰浩特', level: '县级市', description: '内蒙古自治区县级市，兴安盟行政中心，红色之城'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (chengjisihanmiao:Attraction {name: '成吉思汗庙', type: '人文景观', rating: 4.6, opening_hours: '8:30 - 17:00'}),
               (wuyihui址:Attraction {name: '五一会址', type: '人文景观', rating: 4.5, opening_hours: '9:00 - 16:30'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (wlht_kaoyangtui:Food {name: '乌兰浩特烤羊腿', type: '地方特色', price_range: '中', description: '外焦里嫩，香味浓郁'}),
               (chaomi_naicha:Food {name: '炒米奶茶', type: '传统饮品', price_range: '低', description: '咸香可口，营养丰富'}),
               (wulanhaote_binguan:Accommodation {name: '乌兰浩特宾馆', type: '四星级酒店', price_range: '中', rating: 4.4}),
               (wanda_jinhua:Accommodation {name: '乌兰浩特万达锦华酒店', type: '商务酒店', price_range: '中低', rating: 4.2}),
               (wlht_bus:Transportation {name: '乌兰浩特公交', type: '公交', route: '覆盖市区', price: '1-2元'}),
               (wlht_railway:Transportation {name: '乌兰浩特站', type: '火车站', route: '通往白城等地', price: '根据里程'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '乌兰浩特'})
               WHERE a.name IN ['成吉思汗庙', '五一会址']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '乌兰浩特'}), (f:Food)
               WHERE f.name IN ['乌兰浩特烤羊腿', '炒米奶茶']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '成吉思汗庙'}), (f:Food {name: '乌兰浩特烤羊腿'})
               CREATE (a)-[:NEAR_FOOD {distance: '1.5km', tip: '庙区周边蒙餐馆可品尝现烤羊腿'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '成吉思汗庙'}), (f:Food {name: '炒米奶茶'})
               CREATE (a)-[:NEAR_FOOD {distance: '1km', tip: '景区蒙古包体验区可享用传统炒米奶茶'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '五一会址'}), (f:Food {name: '炒米奶茶'})
               CREATE (a)-[:NEAR_FOOD {distance: '800m', tip: '会址附近餐馆可搭配主食品尝奶茶'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '成吉思汗庙'}), (ac:Accommodation {name: '乌兰浩特宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '3km', tip: '适合蒙古族文化体验后舒适休整'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '五一会址'}), (ac:Accommodation {name: '乌兰浩特万达锦华酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '2km', tip: '毗邻红色景点，方便历史文化探访'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '乌兰浩特'}), (t:Transportation)
               WHERE t.name IN ['乌兰浩特公交', '乌兰浩特站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '乌兰浩特公交'}), (t2:Transportation {name: '乌兰浩特站'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '公交直达火车站，方便前往白城、长春等地'}]->(t2)
           """)

        print("乌兰浩特旅游数据导入完成！")

    def import_aershan_data(self):
        """导入阿尔山旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (aes:City {name: '阿尔山', level: '县级市', description: '内蒙古自治区县级市，兴安盟代管，中国最小城市，冰雪之乡'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (aes_forest:Attraction {name: '阿尔山国家森林公园', type: '自然景观', rating: 4.8, opening_hours: '8:00 - 17:00'}),
               (bailangfeng:Attraction {name: '白狼峰', type: '自然景观', rating: 4.6, opening_hours: '全天开放'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (aes_yeShengjun:Food {name: '阿尔山野生菌菇', type: '山珍特产', price_range: '中', description: '味道鲜美，营养丰富'}),
               (lengshuiyu:Food {name: '冷水鱼', type: '地方特色', price_range: '中', description: '肉质细嫩，味道鲜美'}),
               (yurong_guoji:Accommodation {name: '阿尔山御荣国际酒店', type: '四星级酒店', price_range: '中', rating: 4.5}),
               (aershan_binguan:Accommodation {name: '阿尔山宾馆', type: '商务酒店', price_range: '中低', rating: 4.3}),
               (aes_bus:Transportation {name: '阿尔山公交', type: '公交', route: '覆盖市区', price: '1-2元'}),
               (aes_railway:Transportation {name: '阿尔山站', type: '火车站', route: '通往乌兰浩特等地', price: '根据里程'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '阿尔山'})
               WHERE a.name IN ['阿尔山国家森林公园', '白狼峰']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '阿尔山'}), (f:Food)
               WHERE f.name IN ['阿尔山野生菌菇', '冷水鱼']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '阿尔山国家森林公园'}), (f:Food {name: '阿尔山野生菌菇'})
               CREATE (a)-[:NEAR_FOOD {distance: '2km', tip: '景区餐厅有用当日采摘菌菇做的火锅'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '阿尔山国家森林公园'}), (f:Food {name: '冷水鱼'})
               CREATE (a)-[:NEAR_FOOD {distance: '3km', tip: '天池周边餐馆可品尝现捕冷水鱼'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '白狼峰'}), (f:Food {name: '阿尔山野生菌菇'})
               CREATE (a)-[:NEAR_FOOD {distance: '5km', tip: '山脚下农户家可体验菌菇炖菜'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '阿尔山国家森林公园'}), (ac:Accommodation {name: '阿尔山御荣国际酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '15km', tip: '适合火山地貌游览后舒适休整'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '白狼峰'}), (ac:Accommodation {name: '阿尔山宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '10km', tip: '靠近景区，方便自然探秘行程'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '阿尔山'}), (t:Transportation)
               WHERE t.name IN ['阿尔山公交', '阿尔山站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '阿尔山公交'}), (t2:Transportation {name: '阿尔山站'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '公交直达火车站，方便前往乌兰浩特、白城等地'}]->(t2)
           """)

        print("阿尔山旅游数据导入完成！")

    def import_erlianhaote_data(self):
        """导入二连浩特旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (elht:City {name: '二连浩特', level: '县级市', description: '内蒙古自治区县级市，中国对蒙最大陆路口岸，恐龙之乡'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (elht_guomen:Attraction {name: '二连浩特国门', type: '人文景观', rating: 4.6, opening_hours: '8:30 - 17:30'}),
               (konglong_dizhi:Attraction {name: '恐龙地质公园', type: '自然景观', rating: 4.5, opening_hours: '9:00 - 17:00'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (menggu_xianbing:Food {name: '蒙古馅饼', type: '地方特色', price_range: '中低', description: '皮薄馅大，风味独特'}),
               (elht_shoubariu:Food {name: '手把肉', type: '蒙餐', price_range: '中', description: '原汁原味，肉质鲜嫩'}),
               (erlian_guoji:Accommodation {name: '二连浩特国际酒店', type: '四星级酒店', price_range: '中', rating: 4.4}),
               (erlian_kouan:Accommodation {name: '二连浩特口岸大酒店', type: '商务酒店', price_range: '中低', rating: 4.2}),
               (elht_bus:Transportation {name: '二连浩特公交', type: '公交', route: '覆盖市区', price: '1-2元'}),
               (erlian_railway:Transportation {name: '二连站', type: '火车站', route: '通往集宁等地', price: '根据里程'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '二连浩特'})
               WHERE a.name IN ['二连浩特国门', '恐龙地质公园']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '二连浩特'}), (f:Food)
               WHERE f.name IN ['蒙古馅饼', '手把肉']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '二连浩特国门'}), (f:Food {name: '蒙古馅饼'})
               CREATE (a)-[:NEAR_FOOD {distance: '1km', tip: '口岸周边蒙餐馆可品尝现制馅饼'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '二连浩特国门'}), (f:Food {name: '手把肉'})
               CREATE (a)-[:NEAR_FOOD {distance: '1.5km', tip: '景区附近草原餐厅可体验正宗手把肉'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '恐龙地质公园'}), (f:Food {name: '蒙古馅饼'})
               CREATE (a)-[:NEAR_FOOD {distance: '5km', tip: '公园出口小镇有特色馅饼店'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '二连浩特国门'}), (ac:Accommodation {name: '二连浩特国际酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '3km', tip: '适合边境风情体验后舒适休整'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '恐龙地质公园'}), (ac:Accommodation {name: '二连浩特口岸大酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '8km', tip: '靠近景区，方便地质探秘行程'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '二连浩特'}), (t:Transportation)
               WHERE t.name IN ['二连浩特公交', '二连站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '二连浩特公交'}), (t2:Transportation {name: '二连站'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '公交直达火车站，方便前往集宁、呼和浩特等地'}]->(t2)
           """)

        print("二连浩特旅游数据导入完成！")

    def import_xilinhaote_data(self):
        """导入锡林浩特旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (xlht:City {name: '锡林浩特', level: '县级市', description: '内蒙古自治区县级市，锡林郭勒盟行政中心，草原明珠'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (beizimiao:Attraction {name: '贝子庙', type: '人文景观', rating: 4.6, opening_hours: '8:30 - 17:00'}),
               (xilinguole_caoyuan:Attraction {name: '锡林郭勒草原', type: '自然景观', rating: 4.7, opening_hours: '全天开放'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (xlht_shoubariu:Food {name: '手把肉', type: '蒙餐', price_range: '中', description: '原汁原味，肉质鲜嫩'}),
               (xlht_naidoufu:Food {name: '奶豆腐', type: '奶制品', price_range: '低', description: '奶香浓郁，营养丰富'}),
               (xilinhaote_binguan:Accommodation {name: '锡林浩特宾馆', type: '四星级酒店', price_range: '中', rating: 4.5}),
               (xilinguole_fandian:Accommodation {name: '锡林郭勒饭店', type: '四星级酒店', price_range: '中', rating: 4.4}),
               (xlht_bus:Transportation {name: '锡林浩特公交', type: '公交', route: '覆盖市区', price: '1-2元'}),
               (xlht_railway:Transportation {name: '锡林浩特站', type: '火车站', route: '通往呼和浩特等地', price: '根据里程'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '锡林浩特'})
               WHERE a.name IN ['贝子庙', '锡林郭勒草原']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '锡林浩特'}), (f:Food)
               WHERE f.name IN ['手把肉', '奶豆腐']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '锡林郭勒草原'}), (f:Food {name: '手把肉'})
               CREATE (a)-[:NEAR_FOOD {distance: '1km', tip: '草原蒙古包内可品尝现煮手把肉'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '锡林郭勒草原'}), (f:Food {name: '奶豆腐'})
               CREATE (a)-[:NEAR_FOOD {distance: '800m', tip: '牧民家可体验手工奶豆腐制作与品尝'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '贝子庙'}), (f:Food {name: '奶豆腐'})
               CREATE (a)-[:NEAR_FOOD {distance: '1.2km', tip: '庙外市集有传统奶制品摊位'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '贝子庙'}), (ac:Accommodation {name: '锡林浩特宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '2km', tip: '毗邻人文景区，方便文化体验'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '锡林郭勒草原'}), (ac:Accommodation {name: '锡林郭勒饭店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '10km', tip: '适合草原游览后舒适休整，提供特色蒙餐'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '锡林浩特'}), (t:Transportation)
               WHERE t.name IN ['锡林浩特公交', '锡林浩特站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '锡林浩特公交'}), (t2:Transportation {name: '锡林浩特站'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '公交直达火车站，方便前往呼和浩特、二连浩特等地'}]->(t2)
           """)

        print("锡林浩特旅游数据导入完成！")

    def import_shenyang_data(self):
        """导入沈阳旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (sy:City {name: '沈阳', level: '地级市', description: '辽宁省省会，国家历史文化名城，东北地区重要中心城市'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (shenyang_gugong:Attraction {name: '沈阳故宫', type: '人文景观', rating: 4.7, opening_hours: '8:30 - 17:00'}),
               (zhangshi_shuaifu:Attraction {name: '张氏帅府', type: '人文景观', rating: 4.6, opening_hours: '8:00 - 17:30'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (laobian_jiaozi:Food {name: '老边饺子', type: '地方特色', price_range: '中', description: '皮薄馅大，鲜香味美'}),
               (xunrou_dabing:Food {name: '熏肉大饼', type: '传统小吃', price_range: '低', description: '熏香浓郁，饼皮酥脆'}),
               (shenyang_junyue:Accommodation {name: '沈阳君悦酒店', type: '五星级酒店', price_range: '高', rating: 4.7}),
               (shenyang_xianggelila:Accommodation {name: '沈阳香格里拉大酒店', type: '五星级酒店', price_range: '高', rating: 4.6}),
               (shenyang_metro2:Transportation {name: '沈阳地铁2号线', type: '地铁', route: '蒲田路-全运路', price: '2-6元'}),
               (taoxian_dab:Transportation {name: '桃仙机场大巴', type: '机场巴士', route: '市区-桃仙机场', price: '15-20元'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '沈阳'})
               WHERE a.name IN ['沈阳故宫', '张氏帅府']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '沈阳'}), (f:Food)
               WHERE f.name IN ['老边饺子', '熏肉大饼']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '沈阳故宫'}), (f:Food {name: '老边饺子'})
               CREATE (a)-[:NEAR_FOOD {distance: '800m', tip: '中街老店可品尝百年传承饺子'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '沈阳故宫'}), (f:Food {name: '熏肉大饼'})
               CREATE (a)-[:NEAR_FOOD {distance: '500m', tip: '故宫东侧小吃街有地道熏肉大饼'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '张氏帅府'}), (f:Food {name: '老边饺子'})
               CREATE (a)-[:NEAR_FOOD {distance: '1.2km', tip: '帅府周边分店可体验特色馅料'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '沈阳故宫'}), (ac:Accommodation {name: '沈阳君悦酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '2km', tip: '毗邻历史街区，适合文化游览后休整'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '张氏帅府'}), (ac:Accommodation {name: '沈阳香格里拉大酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '1.5km', tip: '靠近历史景点，提供高端住宿体验'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '沈阳'}), (t:Transportation)
               WHERE t.name IN ['沈阳地铁2号线', '桃仙机场大巴']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '沈阳地铁2号线'}), (t2:Transportation {name: '桃仙机场大巴'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '地铁2号线至青年大街站换乘机场大巴，直达桃仙机场'}]->(t2)
           """)

        print("沈阳旅游数据导入完成！")

    def import_dalian_data(self):
        """导入大连旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (dl:City {name: '大连', level: '地级市', description: '辽宁省地级市，北方明珠，浪漫之都，重要港口城市'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (xinghai_guangchang:Attraction {name: '星海广场', type: '人文景观', rating: 4.7, opening_hours: '全天开放'}),
               (laohutan_haiyang:Attraction {name: '老虎滩海洋公园', type: '自然景观', rating: 4.6, opening_hours: '8:00 - 17:00'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (haixian_menzi:Food {name: '海鲜焖子', type: '地方小吃', price_range: '中低', description: '外脆内软，海鲜味浓'}),
               (kao_youyu:Food {name: '烤鱿鱼', type: '海鲜美食', price_range: '中', description: '鲜嫩弹牙，酱香浓郁'}),
               (dalian_junyue:Accommodation {name: '大连君悦酒店', type: '五星级酒店', price_range: '高', rating: 4.7}),
               (dalian_xianggelila:Accommodation {name: '大连香格里拉大酒店', type: '五星级酒店', price_range: '高', rating: 4.6}),
               (dalian_metro2:Transportation {name: '大连地铁2号线', type: '地铁', route: '海之韵-大连北站', price: '2-6元'}),
               (zhoushuizi_dab:Transportation {name: '周水子机场大巴', type: '机场巴士', route: '市区-周水子机场', price: '10-15元'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '大连'})
               WHERE a.name IN ['星海广场', '老虎滩海洋公园']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '大连'}), (f:Food)
               WHERE f.name IN ['海鲜焖子', '烤鱿鱼']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '星海广场'}), (f:Food {name: '海鲜焖子'})
               CREATE (a)-[:NEAR_FOOD {distance: '300m', tip: '广场周边夜市可品尝现做海鲜焖子'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '星海广场'}), (f:Food {name: '烤鱿鱼'})
               CREATE (a)-[:NEAR_FOOD {distance: '500m', tip: '滨海步道旁有现烤鱿鱼摊点'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '老虎滩海洋公园'}), (f:Food {name: '烤鱿鱼'})
               CREATE (a)-[:NEAR_FOOD {distance: '800m', tip: '公园出口处海鲜排档可体验特色烤鱿鱼'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '星海广场'}), (ac:Accommodation {name: '大连君悦酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '1km', tip: '毗邻广场，可享滨海景观与高端服务'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '老虎滩海洋公园'}), (ac:Accommodation {name: '大连香格里拉大酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '5km', tip: '适合海洋公园游览后舒适休整'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '大连'}), (t:Transportation)
               WHERE t.name IN ['大连地铁2号线', '周水子机场大巴']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '大连地铁2号线'}), (t2:Transportation {name: '周水子机场大巴'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '地铁2号线至西安路站换乘机场大巴，直达周水子机场'}]->(t2)
           """)

        print("大连旅游数据导入完成！")

    def import_anshan_data(self):
        """导入鞍山旅游数据导入"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (as:City {name: '鞍山', level: '地级市', description: '辽宁省地级市，中国钢都，玉石之乡'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (qianshan:Attraction {name: '千山风景区', type: '自然景观', rating: 4.7, opening_hours: '8:00 - 17:00'}),
               (yufoyuan:Attraction {name: '玉佛苑', type: '人文景观', rating: 4.5, opening_hours: '8:30 - 16:30'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (anshan_rouzao:Food {name: '鞍山肉枣', type: '地方特产', price_range: '中低', description: '口感鲜美，形似大枣'}),
               (nanguoli:Food {name: '南果梨', type: '地方特产', price_range: '低', description: '果肉细腻，酸甜适口'}),
               (anshan_wanda:Accommodation {name: '鞍山万达嘉华酒店', type: '五星级酒店', price_range: '高', rating: 4.6}),
               (anshan_guoji:Accommodation {name: '鞍山国际大酒店', type: '四星级酒店', price_range: '中', rating: 4.4}),
               (anshan_bus:Transportation {name: '鞍山公交', type: '公交', route: '覆盖市区', price: '1-2元'}),
               (anshan_xi:Transportation {name: '鞍山西站', type: '高铁站', route: '通往沈阳等地', price: '根据里程'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '鞍山'})
               WHERE a.name IN ['千山风景区', '玉佛苑']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '鞍山'}), (f:Food)
               WHERE f.name IN ['鞍山肉枣', '南果梨']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '千山风景区'}), (f:Food {name: '鞍山肉枣'})
               CREATE (a)-[:NEAR_FOOD {distance: '1.5km', tip: '景区入口特产店可购买真空包装肉枣'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '千山风景区'}), (f:Food {name: '南果梨'})
               CREATE (a)-[:NEAR_FOOD {distance: '2km', tip: '山脚下果园可采摘新鲜南果梨'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '玉佛苑'}), (f:Food {name: '南果梨'})
               CREATE (a)-[:NEAR_FOOD {distance: '1km', tip: '景区周边水果店有精品南果梨售卖'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '千山风景区'}), (ac:Accommodation {name: '鞍山万达嘉华酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '8km', tip: '适合山水风光游览后舒适休整'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '玉佛苑'}), (ac:Accommodation {name: '鞍山国际大酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '3km', tip: '靠近人文景区，方便文化探访'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '鞍山'}), (t:Transportation)
               WHERE t.name IN ['鞍山公交', '鞍山西站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '鞍山公交'}), (t2:Transportation {name: '鞍山西站'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '公交专线直达高铁站，方便前往沈阳、大连等地'}]->(t2)
           """)

        print("鞍山旅游数据导入完成！")

    def import_fushun_data(self):
        """导入抚顺旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (fs:City {name: '抚顺', level: '地级市', description: '辽宁省地级市，雷锋之城，中国煤都'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (leifeng_jinianguan:Attraction {name: '雷锋纪念馆', type: '人文景观', rating: 4.6, opening_hours: '9:00 - 16:00'}),
               (hetu阿拉城:Attraction {name: '赫图阿拉城', type: '人文景观', rating: 4.5, opening_hours: '8:30 - 16:30'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (fushun_malaban:Food {name: '抚顺麻辣拌', type: '地方小吃', price_range: '低', description: '麻辣鲜香，配料丰富'}),
               (doumian_juanzi:Food {name: '豆面卷子', type: '传统小吃', price_range: '低', description: '软糯香甜，豆香浓郁'}),
               (fushun_wanda:Accommodation {name: '抚顺万达嘉华酒店', type: '五星级酒店', price_range: '高', rating: 4.5}),
               (fushun_youyi:Accommodation {name: '抚顺友谊宾馆', type: '四星级酒店', price_range: '中', rating: 4.3}),
               (fushun_bus:Transportation {name: '抚顺公交', type: '公交', route: '覆盖市区', price: '1-2元'}),
               (fushun_bei:Transportation {name: '抚顺北站', type: '高铁站', route: '通往沈阳等地', price: '根据里程'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '抚顺'})
               WHERE a.name IN ['雷锋纪念馆', '赫图阿拉城']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '抚顺'}), (f:Food)
               WHERE f.name IN ['抚顺麻辣拌', '豆面卷子']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '赫图阿拉城'}), (f:Food {name: '抚顺麻辣拌'})
               CREATE (a)-[:NEAR_FOOD {distance: '1km', tip: '古城商业街可品尝特色麻辣拌'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '赫图阿拉城'}), (f:Food {name: '豆面卷子'})
               CREATE (a)-[:NEAR_FOOD {distance: '800m', tip: '景区内满族风味店有传统豆面卷子'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '雷锋纪念馆'}), (f:Food {name: '抚顺麻辣拌'})
               CREATE (a)-[:NEAR_FOOD {distance: '1.5km', tip: '纪念馆周边小吃街可体验地道口味'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '雷锋纪念馆'}), (ac:Accommodation {name: '抚顺万达嘉华酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '3km', tip: '适合红色文化体验后舒适休整'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '赫图阿拉城'}), (ac:Accommodation {name: '抚顺友谊宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '10km', tip: '靠近历史古城，方便清前文化探访'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '抚顺'}), (t:Transportation)
               WHERE t.name IN ['抚顺公交', '抚顺北站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '抚顺公交'}), (t2:Transportation {name: '抚顺北站'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '公交直达高铁站，方便前往沈阳、长春等地'}]->(t2)
           """)

        print("抚顺旅游数据导入完成！")

    def import_benxi_data(self):
        """导入本溪旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (bx:City {name: '本溪', level: '地级市', description: '辽宁省地级市，中国枫叶之都，钢铁之城'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (benxi_shuidong:Attraction {name: '本溪水洞', type: '自然景观', rating: 4.7, opening_hours: '8:30 - 16:30'}),
               (guanmenshan:Attraction {name: '关门山', type: '自然景观', rating: 4.6, opening_hours: '8:00 - 17:00'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (xiaoshi_yangtang:Food {name: '小市羊汤', type: '地方特色', price_range: '中低', description: '汤鲜味美，暖胃驱寒'}),
               (changkuan_zhuti:Food {name: '长宽猪蹄', type: '传统美食', price_range: '中低', description: '软烂入味，肥而不腻'}),
               (benxi_fuhong:Accommodation {name: '本溪富虹国际饭店', type: '五星级酒店', price_range: '高', rating: 4.6}),
               (benxi_binguan:Accommodation {name: '本溪宾馆', type: '四星级酒店', price_range: '中', rating: 4.4}),
               (benxi_bus:Transportation {name: '本溪公交', type: '公交', route: '覆盖市区', price: '1-2元'}),
               (benxi_railway:Transportation {name: '本溪站', type: '火车站', route: '通往沈阳等地', price: '根据里程'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '本溪'})
               WHERE a.name IN ['本溪水洞', '关门山']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '本溪'}), (f:Food)
               WHERE f.name IN ['小市羊汤', '长宽猪蹄']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '关门山'}), (f:Food {name: '小市羊汤'})
               CREATE (a)-[:NEAR_FOOD {distance: '3km', tip: '景区出口小镇有百年羊汤老店'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '关门山'}), (f:Food {name: '长宽猪蹄'})
               CREATE (a)-[:NEAR_FOOD {distance: '4km', tip: '山脚下餐馆可搭配主食品尝猪蹄'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '本溪水洞'}), (f:Food {name: '小市羊汤'})
               CREATE (a)-[:NEAR_FOOD {distance: '2km', tip: '水洞景区周边可享用热乎羊汤驱寒'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '本溪水洞'}), (ac:Accommodation {name: '本溪富虹国际饭店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '15km', tip: '适合溶洞探险后舒适休整'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '关门山'}), (ac:Accommodation {name: '本溪宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '10km', tip: '靠近枫叶景区，方便秋季赏枫行程'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '本溪'}), (t:Transportation)
               WHERE t.name IN ['本溪公交', '本溪站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '本溪公交'}), (t2:Transportation {name: '本溪站'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '公交直达火车站，方便前往沈阳、鞍山等地'}]->(t2)
           """)

        print("本溪旅游数据导入完成！")

    def import_dandong_data(self):
        """导入丹东旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (dd:City {name: '丹东', level: '地级市', description: '辽宁省地级市，中国最大边境城市，英雄城市'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (yalujiang_duanqiao:Attraction {name: '鸭绿江断桥', type: '人文景观', rating: 4.7, opening_hours: '8:00 - 17:00'}),
               (kangmei_yuanchao:Attraction {name: '抗美援朝纪念馆', type: '人文景观', rating: 4.6, opening_hours: '9:00 - 16:00'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (dandong_huangxianzi:Food {name: '丹东黄蚬子', type: '地方特产', price_range: '中', description: '肉质鲜美，营养丰富'}),
               (hanshi_kaorou:Food {name: '韩式烤肉', type: '异国风味', price_range: '中高', description: '风味独特，肉质鲜嫩'}),
               (dandong_furuide:Accommodation {name: '丹东福瑞德大酒店', type: '五星级酒店', price_range: '高', rating: 4.6}),
               (dandong_zhonglian:Accommodation {name: '丹东中联大酒店', type: '四星级酒店', price_range: '中', rating: 4.4}),
               (dandong_bus:Transportation {name: '丹东公交', type: '公交', route: '覆盖市区', price: '1-2元'}),
               (dandong_railway:Transportation {name: '丹东站', type: '火车站', route: '通往沈阳等地', price: '根据里程'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '丹东'})
               WHERE a.name IN ['鸭绿江断桥', '抗美援朝纪念馆']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '丹东'}), (f:Food)
               WHERE f.name IN ['丹东黄蚬子', '韩式烤肉']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '鸭绿江断桥'}), (f:Food {name: '丹东黄蚬子'})
               CREATE (a)-[:NEAR_FOOD {distance: '500m', tip: '江边大排档可品尝现炒黄蚬子'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '鸭绿江断桥'}), (f:Food {name: '韩式烤肉'})
               CREATE (a)-[:NEAR_FOOD {distance: '1.2km', tip: '边境风情街有正宗韩式烤肉店'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '抗美援朝纪念馆'}), (f:Food {name: '韩式烤肉'})
               CREATE (a)-[:NEAR_FOOD {distance: '2km', tip: '纪念馆周边有多家韩式风味餐馆'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '鸭绿江断桥'}), (ac:Accommodation {name: '丹东福瑞德大酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '1.5km', tip: '毗邻江边，可享边境风光与高端服务'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '抗美援朝纪念馆'}), (ac:Accommodation {name: '丹东中联大酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '3km', tip: '靠近红色景点，方便历史文化探访'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '丹东'}), (t:Transportation)
               WHERE t.name IN ['丹东公交', '丹东站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '丹东公交'}), (t2:Transportation {name: '丹东站'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '公交直达火车站，方便前往沈阳、大连等地'}]->(t2)
           """)

        print("丹东旅游数据导入完成！")

    def import_jinzhou_data(self):
        """导入锦州旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (jz:City {name: '锦州', level: '地级市', description: '辽宁省地级市，辽西中心城市，英雄城市'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (liaoshen_zhanyi:Attraction {name: '辽沈战役纪念馆', type: '人文景观', rating: 4.7, opening_hours: '9:00 - 16:00'}),
               (bijia_shan:Attraction {name: '笔架山', type: '自然景观', rating: 4.6, opening_hours: '8:00 - 17:00'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (jinzhou_shaokao:Food {name: '锦州烧烤', type: '地方特色', price_range: '中低', description: '风味独特，品种丰富'}),
               (beizhen_zhuti:Food {name: '北镇猪蹄', type: '传统美食', price_range: '中低', description: '软烂入味，肥而不腻'}),
               (jinzhou_xilaideng:Accommodation {name: '锦州喜来登酒店', type: '五星级酒店', price_range: '高', rating: 4.6}),
               (jinzhou_binguan:Accommodation {name: '锦州宾馆', type: '四星级酒店', price_range: '中', rating: 4.4}),
               (jinzhou_bus:Transportation {name: '锦州公交', type: '公交', route: '覆盖市区', price: '1-2元'}),
               (jinzhou_nan:Transportation {name: '锦州南站', type: '高铁站', route: '通往沈阳等地', price: '根据里程'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '锦州'})
               WHERE a.name IN ['辽沈战役纪念馆', '笔架山']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '锦州'}), (f:Food)
               WHERE f.name IN ['锦州烧烤', '北镇猪蹄']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '笔架山'}), (f:Food {name: '锦州烧烤'})
               CREATE (a)-[:NEAR_FOOD {distance: '2km', tip: '海滨浴场周边有海鲜烧烤大排档'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '笔架山'}), (f:Food {name: '北镇猪蹄'})
               CREATE (a)-[:NEAR_FOOD {distance: '3km', tip: '景区出口特产店可购买真空包装猪蹄'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '辽沈战役纪念馆'}), (f:Food {name: '锦州烧烤'})
               CREATE (a)-[:NEAR_FOOD {distance: '1.5km', tip: '纪念馆周边有多家老字号烧烤店'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '辽沈战役纪念馆'}), (ac:Accommodation {name: '锦州喜来登酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '2km', tip: '适合红色文化体验后舒适休整'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '笔架山'}), (ac:Accommodation {name: '锦州宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '10km', tip: '靠近海岸景区，方便海滨游览行程'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '锦州'}), (t:Transportation)
               WHERE t.name IN ['锦州公交', '锦州南站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '锦州公交'}), (t2:Transportation {name: '锦州南站'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '公交专线直达高铁站，方便前往沈阳、北京等地'}]->(t2)
           """)

        print("锦州旅游数据导入完成！")

    def import_yingkou_data(self):
        """导入营口旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (yk:City {name: '营口', level: '地级市', description: '辽宁省地级市，东北最早开埠口岸，百年港城'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (liaohe_laojie:Attraction {name: '辽河老街', type: '人文景观', rating: 4.5, opening_hours: '全天开放'}),
               (shanhai_guangchang:Attraction {name: '山海广场', type: '人文景观', rating: 4.4, opening_hours: '8:00 - 17:00'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (yingkou_haixian:Food {name: '营口海鲜', type: '地方特色', price_range: '中', description: '新鲜美味，品种丰富'}),
               (yingkou_dajiang:Food {name: '营口大酱', type: '地方特产', price_range: '低', description: '酱香浓郁，风味独特'}),
               (yingkou_wanda:Accommodation {name: '营口万达嘉华酒店', type: '五星级酒店', price_range: '高', rating: 4.6}),
               (yingkou_guoji:Accommodation {name: '营口国际酒店', type: '四星级酒店', price_range: '中', rating: 4.4}),
               (yingkou_bus:Transportation {name: '营口公交', type: '公交', route: '覆盖市区', price: '1-2元'}),
               (yingkou_dong:Transportation {name: '营口东站', type: '高铁站', route: '通往大连等地', price: '根据里程'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '营口'})
               WHERE a.name IN ['辽河老街', '山海广场']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '营口'}), (f:Food)
               WHERE f.name IN ['营口海鲜', '营口大酱']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '辽河老街'}), (f:Food {name: '营口海鲜'})
               CREATE (a)-[:NEAR_FOOD {distance: '500m', tip: '老街内海鲜餐馆可品尝当日海产'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '辽河老街'}), (f:Food {name: '营口大酱'})
               CREATE (a)-[:NEAR_FOOD {distance: '300m', tip: '百年酱园可体验传统工艺大酱'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '山海广场'}), (f:Food {name: '营口海鲜'})
               CREATE (a)-[:NEAR_FOOD {distance: '800m', tip: '海滨大排档可享用现捞海鲜'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '辽河老街'}), (ac:Accommodation {name: '营口万达嘉华酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '1.5km', tip: '毗邻百年商埠，适合文化体验后休整'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '山海广场'}), (ac:Accommodation {name: '营口国际酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '5km', tip: '靠近海滨景区，方便休闲游览'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '营口'}), (t:Transportation)
               WHERE t.name IN ['营口公交', '营口东站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '营口公交'}), (t2:Transportation {name: '营口东站'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '公交专线直达高铁站，方便前往大连、沈阳等地'}]->(t2)
           """)

        print("营口旅游数据导入完成！")

    def import_fuxin_data(self):
        """导入阜新旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (fx:City {name: '阜新', level: '地级市', description: '辽宁省地级市，中国玛瑙之都，转型示范城市'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (haitangshan_moya:Attraction {name: '海棠山摩崖造像', type: '人文景观', rating: 4.5, opening_hours: '8:30 - 16:30'}),
               (ruiying_si:Attraction {name: '瑞应寺', type: '人文景观', rating: 4.4, opening_hours: '8:00 - 17:00'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (fuxin_xuntu:Food {name: '阜新熏兔', type: '地方特色', price_range: '中低', description: '熏香浓郁，肉质鲜嫩'}),
               (lama_gao:Food {name: '喇嘛糕', type: '传统糕点', price_range: '低', description: '松软香甜，入口即化'}),
               (fuxin_baodi:Accommodation {name: '阜新宝地温泉酒店', type: '四星级酒店', price_range: '中', rating: 4.4}),
               (fuxin_guomao:Accommodation {name: '阜新国贸大酒店', type: '商务酒店', price_range: '中低', rating: 4.2}),
               (fuxin_bus:Transportation {name: '阜新公交', type: '公交', route: '覆盖市区', price: '1-2元'}),
               (fuxin_railway:Transportation {name: '阜新站', type: '火车站', route: '通往沈阳等地', price: '根据里程'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '阜新'})
               WHERE a.name IN ['海棠山摩崖造像', '瑞应寺']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '阜新'}), (f:Food)
               WHERE f.name IN ['阜新熏兔', '喇嘛糕']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '海棠山摩崖造像'}), (f:Food {name: '阜新熏兔'})
               CREATE (a)-[:NEAR_FOOD {distance: '2km', tip: '景区山脚下餐馆可品尝现制熏兔'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '海棠山摩崖造像'}), (f:Food {name: '喇嘛糕'})
               CREATE (a)-[:NEAR_FOOD {distance: '1.5km', tip: '佛教文化街有传统喇嘛糕售卖'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '瑞应寺'}), (f:Food {name: '喇嘛糕'})
               CREATE (a)-[:NEAR_FOOD {distance: '800m', tip: '寺外商铺可体验寺庙传统糕点'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '海棠山摩崖造像'}), (ac:Accommodation {name: '阜新宝地温泉酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '10km', tip: '适合佛教文化体验后温泉休整'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '瑞应寺'}), (ac:Accommodation {name: '阜新国贸大酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '5km', tip: '靠近宗教景区，方便文化探访'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '阜新'}), (t:Transportation)
               WHERE t.name IN ['阜新公交', '阜新站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '阜新公交'}), (t2:Transportation {name: '阜新站'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '公交直达火车站，方便前往沈阳、锦州等地'}]->(t2)
           """)

        print("阜新旅游数据导入完成！")

    def import_liaoyang_data(self):
        """导入辽阳旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (ly:City {name: '辽阳', level: '地级市', description: '辽宁省地级市，东北最古老城市，千年古城'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (liaoyang_baita:Attraction {name: '辽阳白塔', type: '人文景观', rating: 4.6, opening_hours: '8:30 - 16:30'}),
               (dongjingling:Attraction {name: '东京陵', type: '人文景观', rating: 4.5, opening_hours: '9:00 - 16:00'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (tatang:Food {name: '塔糖', type: '地方特产', price_range: '低', description: '酥脆香甜，历史悠久'}),
               (laoyangtou_shaoji:Food {name: '老杨头烧鸡', type: '传统美食', price_range: '中低', description: '色泽红亮，香味浓郁'}),
               (liaoyang_fuhong:Accommodation {name: '辽阳富虹国际饭店', type: '五星级酒店', price_range: '高', rating: 4.6}),
               (liaoyang_binguan:Accommodation {name: '辽阳宾馆', type: '四星级酒店', price_range: '中', rating: 4.4}),
               (liaoyang_bus:Transportation {name: '辽阳公交', type: '公交', route: '覆盖市区', price: '1-2元'}),
               (liaoyang_railway:Transportation {name: '辽阳站', type: '火车站', route: '通往沈阳等地', price: '根据里程'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '辽阳'})
               WHERE a.name IN ['辽阳白塔', '东京陵']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '辽阳'}), (f:Food)
               WHERE f.name IN ['塔糖', '老杨头烧鸡']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '辽阳白塔'}), (f:Food {name: '塔糖'})
               CREATE (a)-[:NEAR_FOOD {distance: '300m', tip: '白塔周边老字号店铺可购传统塔糖'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '辽阳白塔'}), (f:Food {name: '老杨头烧鸡'})
               CREATE (a)-[:NEAR_FOOD {distance: '800m', tip: '古城商业街有正宗老杨头烧鸡店'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '东京陵'}), (f:Food {name: '老杨头烧鸡'})
               CREATE (a)-[:NEAR_FOOD {distance: '2km', tip: '景区周边食品店可购真空包装烧鸡'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '辽阳白塔'}), (ac:Accommodation {name: '辽阳富虹国际饭店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '2km', tip: '毗邻千年古塔，适合历史文化体验后休整'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '东京陵'}), (ac:Accommodation {name: '辽阳宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '4km', tip: '靠近历史遗迹，方便文化探访行程'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '辽阳'}), (t:Transportation)
               WHERE t.name IN ['辽阳公交', '辽阳站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '辽阳公交'}), (t2:Transportation {name: '辽阳站'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '公交直达火车站，方便前往沈阳、鞍山等地'}]->(t2)
           """)

        print("辽阳旅游数据导入完成！")

    def import_panjin_data(self):
        """导入盘锦旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (pj:City {name: '盘锦', level: '地级市', description: '辽宁省地级市，湿地之都，中国蟹都'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (honghaitan:Attraction {name: '红海滩', type: '自然景观', rating: 4.7, opening_hours: '8:00 - 17:00'}),
               (dingxiang_shengtai:Attraction {name: '鼎翔生态旅游区', type: '自然景观', rating: 4.5, opening_hours: '8:30 - 16:30'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (panjin_hexie:Food {name: '盘锦河蟹', type: '地方特产', price_range: '中高', description: '膏满黄肥，鲜美无比'}),
               (panjin_dami:Food {name: '大米', type: '地方特产', price_range: '低', description: '米粒饱满，口感香糯'}),
               (panjin_ruishi:Accommodation {name: '盘锦瑞诗酒店', type: '五星级酒店', price_range: '高', rating: 4.6}),
               (panjin_guomao:Accommodation {name: '盘锦国贸饭店', type: '四星级酒店', price_range: '中', rating: 4.4}),
               (panjin_bus:Transportation {name: '盘锦公交', type: '公交', route: '覆盖市区', price: '1-2元'}),
               (panjin_railway:Transportation {name: '盘锦站', type: '火车站', route: '通往沈阳等地', price: '根据里程'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '盘锦'})
               WHERE a.name IN ['红海滩', '鼎翔生态旅游区']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '盘锦'}), (f:Food)
               WHERE f.name IN ['盘锦河蟹', '大米']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '红海滩'}), (f:Food {name: '盘锦河蟹'})
               CREATE (a)-[:NEAR_FOOD {distance: '1.5km', tip: '景区周边蟹庄可品尝现蒸河蟹'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '红海滩'}), (f:Food {name: '大米'})
               CREATE (a)-[:NEAR_FOOD {distance: '3km', tip: '湿地稻田可体验现磨新米'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '鼎翔生态旅游区'}), (f:Food {name: '盘锦河蟹'})
               CREATE (a)-[:NEAR_FOOD {distance: '2km', tip: '生态园区内可参与捕蟹并现场烹饪'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '红海滩'}), (ac:Accommodation {name: '盘锦瑞诗酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '20km', tip: '适合湿地景观游览后舒适休整，提供河蟹特色餐'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '鼎翔生态旅游区'}), (ac:Accommodation {name: '盘锦国贸饭店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '15km', tip: '靠近生态景区，方便自然研学行程'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '盘锦'}), (t:Transportation)
               WHERE t.name IN ['盘锦公交', '盘锦站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '盘锦公交'}), (t2:Transportation {name: '盘锦站'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '公交直达火车站，方便前往沈阳、大连等地'}]->(t2)
           """)

        print("盘锦旅游数据导入完成！")

    def import_tieling_data(self):
        """导入铁岭旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (tl:City {name: '铁岭', level: '地级市', description: '辽宁省地级市，较大城市，小品艺术之乡'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (longshoushan:Attraction {name: '龙首山', type: '自然景观', rating: 4.5, opening_hours: '全天开放'}),
               (yingang_shuyuan:Attraction {name: '银冈书院', type: '人文景观', rating: 4.4, opening_hours: '9:00 - 16:30'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (tieling_huoshao:Food {name: '铁岭火勺', type: '地方小吃', price_range: '低', description: '外酥里嫩，馅料丰富'}),
               (lijitan_rou:Food {name: '李记坛肉', type: '传统美食', price_range: '中低', description: '肉质酥烂，肥而不腻'}),
               (tieling_jincheng:Accommodation {name: '铁岭金城粤海国际酒店', type: '四星级酒店', price_range: '中', rating: 4.4}),
               (tieling_fandian:Accommodation {name: '铁岭饭店', type: '商务酒店', price_range: '中低', rating: 4.2}),
               (tieling_bus:Transportation {name: '铁岭公交', type: '公交', route: '覆盖市区', price: '1-2元'}),
               (tieling_xi:Transportation {name: '铁岭西站', type: '高铁站', route: '通往沈阳等地', price: '根据里程'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '铁岭'})
               WHERE a.name IN ['龙首山', '银冈书院']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '铁岭'}), (f:Food)
               WHERE f.name IN ['铁岭火勺', '李记坛肉']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '龙首山'}), (f:Food {name: '铁岭火勺'})
               CREATE (a)-[:NEAR_FOOD {distance: '500m', tip: '山脚下小吃街可品尝现烙火勺'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '龙首山'}), (f:Food {name: '李记坛肉'})
               CREATE (a)-[:NEAR_FOOD {distance: '800m', tip: '山脚老字号餐馆可搭配米饭食用坛肉'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '银冈书院'}), (f:Food {name: '铁岭火勺'})
               CREATE (a)-[:NEAR_FOOD {distance: '1km', tip: '书院周边早餐店有传统火勺供应'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '龙首山'}), (ac:Accommodation {name: '铁岭金城粤海国际酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '2km', tip: '毗邻自然景区，适合登高游览后休整'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '银冈书院'}), (ac:Accommodation {name: '铁岭饭店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '1.5km', tip: '靠近人文景点，方便文化探访行程'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '铁岭'}), (t:Transportation)
               WHERE t.name IN ['铁岭公交', '铁岭西站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '铁岭公交'}), (t2:Transportation {name: '铁岭西站'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '公交专线直达高铁站，方便前往沈阳、长春等地'}]->(t2)
           """)

        print("铁岭旅游数据导入完成！")

    def import_huludao_data(self):
        """导入葫芦岛旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (hld:City {name: '葫芦岛', level: '地级市', description: '辽宁省地级市，关外第一第一市，滨海城市'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (xingcheng_gucheng:Attraction {name: '兴城古城', type: '人文景观', rating: 4.6, opening_hours: '8:30 - 17:00'}),
               (longwan_haibin:Attraction {name: '龙湾海滨', type: '自然景观', rating: 4.5, opening_hours: '全天开放'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (huludao_haixian:Food {name: '海鲜', type: '地方特色', price_range: '中', description: '新鲜美味，品种丰富'}),
               (hongluoxian_gandoufu:Food {name: '虹螺岘干豆腐', type: '地方特产', price_range: '低', description: '薄而韧，豆香浓郁'}),
               (huludao_guoji:Accommodation {name: '葫芦岛国际酒店', type: '四星级酒店', price_range: '中', rating: 4.5}),
               (huludao_binguan:Accommodation {name: '葫芦岛宾馆', type: '商务酒店', price_range: '中低', rating: 4.3}),
               (huludao_bus:Transportation {name: '葫芦岛公交', type: '公交', route: '覆盖市区', price: '1-2元'}),
               (huludao_bei:Transportation {name: '葫芦岛北站', type: '高铁站', route: '通往沈阳等地', price: '根据里程'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '葫芦岛'})
               WHERE a.name IN ['兴城古城', '龙湾海滨']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '葫芦岛'}), (f:Food)
               WHERE f.name IN ['海鲜', '虹螺岘干豆腐']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '龙湾海滨'}), (f:Food {name: '海鲜'})
               CREATE (a)-[:NEAR_FOOD {distance: '300m', tip: '海滨浴场周边有海鲜大排档，现捞现做'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '龙湾海滨'}), (f:Food {name: '虹螺岘干豆腐'})
               CREATE (a)-[:NEAR_FOOD {distance: '2km', tip: '海滨市集可购买真空包装干豆腐作伴手礼'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '兴城古城'}), (f:Food {name: '海鲜'})
               CREATE (a)-[:NEAR_FOOD {distance: '1.5km', tip: '古城外海鲜餐馆可品尝当地特色海产'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '龙湾海滨'}), (ac:Accommodation {name: '葫芦岛国际酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '1km', tip: '毗邻海滨，可享海景与舒适住宿体验'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '兴城古城'}), (ac:Accommodation {name: '葫芦岛宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '3km', tip: '靠近古城景区，方便历史文化探访'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '葫芦岛'}), (t:Transportation)
               WHERE t.name IN ['葫芦岛公交', '葫芦岛北站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '葫芦岛公交'}), (t2:Transportation {name: '葫芦岛北站'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '公交专线直达高铁站，方便前往沈阳、北京等地'}]->(t2)
           """)

        print("葫芦岛旅游数据导入完成！")

    def import_xinmin_data(self):
        """导入新民旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (xm:City {name: '新民', level: '县级市', description: '辽宁省县级市，沈阳代管，辽河沿岸重要城市'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (xinmin_sannong:Attraction {name: '新民三农博览园', type: '农业观光', rating: 4.4, opening_hours: '8:30 - 16:30'}),
               (liaobin_ta:Attraction {name: '辽滨塔', type: '人文景观', rating: 4.3, opening_hours: '9:00 - 16:00'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (xinmin_xuechang:Food {name: '新民血肠', type: '地方特色', price_range: '中低', description: '口感独特，香味浓郁'}),
               (liangshan_xigua:Food {name: '梁山西瓜', type: '地方特产', price_range: '低', description: '汁多味甜，品质优良'}),
               (xinmin_binguan:Accommodation {name: '新民宾馆', type: '三星级酒店', price_range: '中低', rating: 4.3}),
               (xinmin_jinshan:Accommodation {name: '新民金山宾馆', type: '商务酒店', price_range: '中低', rating: 4.2}),
               (xinmin_bus:Transportation {name: '新民公交', type: '公交', route: '覆盖市区', price: '1-2元'}),
               (xinmin_railway:Transportation {name: '新民站', type: '火车站', route: '通往沈阳等地', price: '根据里程'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '新民'})
               WHERE a.name IN ['新民三农博览园', '辽滨塔']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '新民'}), (f:Food)
               WHERE f.name IN ['新民血肠', '梁山西瓜']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '新民三农博览园'}), (f:Food {name: '新民血肠'})
               CREATE (a)-[:NEAR_FOOD {distance: '1km', tip: '博览园餐饮区可品尝特色血肠炖菜'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '新民三农博览园'}), (f:Food {name: '梁山西瓜'})
               CREATE (a)-[:NEAR_FOOD {distance: '500m', tip: '园区内瓜果区可体验现摘西瓜'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '辽滨塔'}), (f:Food {name: '梁山西瓜'})
               CREATE (a)-[:NEAR_FOOD {distance: '3km', tip: '塔周边农家店有新鲜西瓜售卖'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '新民三农博览园'}), (ac:Accommodation {name: '新民宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '4km', tip: '适合农业文化体验后休整，提供农家菜'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '辽滨塔'}), (ac:Accommodation {name: '新民金山宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '6km', tip: '靠近历史景点，方便文化探访'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '新民'}), (t:Transportation)
               WHERE t.name IN ['新民公交', '新民站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '新民公交'}), (t2:Transportation {name: '新民站'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '公交直达火车站，方便前往沈阳、锦州等地'}]->(t2)
           """)

        print("新民旅游数据导入完成！")

    def import_wafangdian_data(self):
        """导入瓦房店旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (wfd:City {name: '瓦房店', level: '县级市', description: '辽宁省县级市，大连代管，中国轴承之都'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (xianyuwan:Attraction {name: '仙浴湾', type: '自然景观', rating: 4.5, opening_hours: '全天开放'}),
               (longwangmiao:Attraction {name: '龙王庙', type: '人文景观', rating: 4.3, opening_hours: '8:30 - 16:30'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (wafangdian_pingguo:Food {name: '瓦房店苹果', type: '地方特产', price_range: '低', description: '脆甜多汁，品质优良'}),
               (wafangdian_haixian:Food {name: '海鲜', type: '地方特色', price_range: '中', description: '新鲜美味，品种丰富'}),
               (wafangdian_yuanzhou:Accommodation {name: '瓦房店远洲大酒店', type: '四星级酒店', price_range: '中', rating: 4.4}),
               (wafangdian_binguan:Accommodation {name: '瓦房店宾馆', type: '商务酒店', price_range: '中低', rating: 4.2}),
               (wafangdian_bus:Transportation {name: '瓦房店公交', type: '公交', route: '覆盖市区', price: '1-2元'}),
               (wafangdian_xi:Transportation {name: '瓦房店西站', type: '高铁站', route: '通往大连等地', price: '根据里程'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '瓦房店'})
               WHERE a.name IN ['仙浴湾', '龙王庙']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '瓦房店'}), (f:Food)
               WHERE f.name IN ['瓦房店苹果', '海鲜']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '仙浴湾'}), (f:Food {name: '海鲜'})
               CREATE (a)-[:NEAR_FOOD {distance: '500m', tip: '海滨度假村内可享用现捕海鲜'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '仙浴湾'}), (f:Food {name: '瓦房店苹果'})
               CREATE (a)-[:NEAR_FOOD {distance: '3km', tip: '海滨市集有本地苹果直销点'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '龙王庙'}), (f:Food {name: '海鲜'})
               CREATE (a)-[:NEAR_FOOD {distance: '2km', tip: '寺庙周边渔家餐馆可品尝特色海鲜'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '仙浴湾'}), (ac:Accommodation {name: '瓦房店远洲大酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '8km', tip: '适合海滨度假后舒适休整，提供海鲜盛宴'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '龙王庙'}), (ac:Accommodation {name: '瓦房店宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '5km', tip: '靠近人文景点，方便文化探访行程'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '瓦房店'}), (t:Transportation)
               WHERE t.name IN ['瓦房店公交', '瓦房店西站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '瓦房店公交'}), (t2:Transportation {name: '瓦房店西站'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '公交专线直达高铁站，方便前往大连、沈阳等地'}]->(t2)
           """)

        print("瓦房店旅游数据导入完成！")

    def import_zhuanghe_data(self):
        """导入庄河旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (zh:City {name: '庄河', level: '县级市', description: '辽宁省县级市，大连代管，中国蓝莓之乡'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (bingyugou:Attraction {name: '冰峪沟', type: '自然景观', rating: 4.6, opening_hours: '8:00 - 17:00'}),
               (haiwang_jiudao:Attraction {name: '海王九岛', type: '自然景观', rating: 4.5, opening_hours: '全天开放'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (zhuanghe_lanmei:Food {name: '庄河蓝莓', type: '地方特产', price_range: '中低', description: '果肉细腻，酸甜适口'}),
               (zhuanghe_haixian:Food {name: '庄河海鲜', type: '地方特色', price_range: '中', description: '新鲜肥美，品种丰富'}),
               (zhuanghe_huayun:Accommodation {name: '庄河华韵宾馆', type: '三星级酒店', price_range: '中低', rating: 4.3}),
               (zhuanghe_jinyuan:Accommodation {name: '庄河金元大酒店', type: '商务酒店', price_range: '中低', rating: 4.2}),
               (zhuanghe_bus:Transportation {name: '庄河公交', type: '公交', route: '覆盖市区', price: '1-2元'}),
               (zhuanghe_bei:Transportation {name: '庄河北站', type: '高铁站', route: '通往大连等地', price: '根据里程'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '庄河'})
               WHERE a.name IN ['冰峪沟', '海王九岛']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '庄河'}), (f:Food)
               WHERE f.name IN ['庄河蓝莓', '庄河海鲜']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '海王九岛'}), (f:Food {name: '庄河海鲜'})
               CREATE (a)-[:NEAR_FOOD {distance: '300m', tip: '海岛码头周边渔家餐馆可品尝现捕海鲜'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '海王九岛'}), (f:Food {name: '庄河蓝莓'})
               CREATE (a)-[:NEAR_FOOD {distance: '5km', tip: '岛外蓝莓种植园可体验采摘'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '冰峪沟'}), (f:Food {name: '庄河海鲜'})
               CREATE (a)-[:NEAR_FOOD {distance: '8km', tip: '景区出口小镇有河鲜海鲜融合菜馆'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '冰峪沟'}), (ac:Accommodation {name: '庄河华韵宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '10km', tip: '适合山水游览后休整，提供蓝莓甜品'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '海王九岛'}), (ac:Accommodation {name: '庄河金元大酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '15km', tip: '靠近海岛码头，方便海岛观光行程'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '庄河'}), (t:Transportation)
               WHERE t.name IN ['庄河公交', '庄河北站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '庄河公交'}), (t2:Transportation {name: '庄河北站'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '公交专线直达高铁站，方便前往大连、沈阳等地'}]->(t2)
           """)

        print("庄河旅游数据导入完成！")

    def import_haicheng_data(self):
        """导入海城旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (hc:City {name: '海城', level: '县级市', description: '辽宁省县级市，鞍山代管，中国菱镁之乡，滑石之都'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (baiyunshan:Attraction {name: '白云山', type: '自然景观', rating: 4.5, opening_hours: '8:00 - 17:00'}),
               (cuoshishan_gongyuan:Attraction {name: '厝石山公园', type: '人文景观', rating: 4.4, opening_hours: '全天开放'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (haicheng_xianbing:Food {name: '海城馅饼', type: '地方小吃', price_range: '低', description: '皮薄馅大，鲜香味美'}),
               (niuzhuang_techan:Food {name: '牛庄特产', type: '地方特色', price_range: '中低', description: '风味独特，历史悠久'}),
               (haicheng_guoji:Accommodation {name: '海城国际酒店', type: '四星级酒店', price_range: '中', rating: 4.4}),
               (haicheng_binguan:Accommodation {name: '海城宾馆', type: '商务酒店', price_range: '中低', rating: 4.2}),
               (haicheng_bus:Transportation {name: '海城公交', type: '公交', route: '覆盖市区', price: '1-2元'}),
               (haicheng_xi:Transportation {name: '海城西站', type: '高铁站', route: '通往沈阳等地', price: '根据里程'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '海城'})
               WHERE a.name IN ['白云山', '厝石山公园']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '海城'}), (f:Food)
               WHERE f.name IN ['海城馅饼', '牛庄特产']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '厝石山公园'}), (f:Food {name: '海城馅饼'})
               CREATE (a)-[:NEAR_FOOD {distance: '400m', tip: '公园门口老字号馅饼店可现做现吃'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '厝石山公园'}), (f:Food {name: '牛庄特产'})
               CREATE (a)-[:NEAR_FOOD {distance: '600m', tip: '公园周边特产店可选购牛庄特色食品'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '白云山'}), (f:Food {name: '海城馅饼'})
               CREATE (a)-[:NEAR_FOOD {distance: '3km', tip: '山脚下农家乐可搭配山野菜馅馅饼'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '白云山'}), (ac:Accommodation {name: '海城国际酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '12km', tip: '适合山水游览后舒适休整，提供馅饼早餐'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '厝石山公园'}), (ac:Accommodation {name: '海城宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '1km', tip: '靠近园林景点，方便休闲游览行程'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '海城'}), (t:Transportation)
               WHERE t.name IN ['海城公交', '海城西站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '海城公交'}), (t2:Transportation {name: '海城西站'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '公交专线直达高铁站，方便前往沈阳、鞍山等地'}]->(t2)
           """)

        print("海城旅游数据导入完成！")

    def import_donggang_data(self):
        """导入东港旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (dg:City {name: '东港', level: '县级市', description: '辽宁省县级市，丹东代管，中国海岸线北端起点'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (daludao:Attraction {name: '大鹿岛', type: '自然景观', rating: 4.6, opening_hours: '全天开放'}),
               (zhangdao:Attraction {name: '獐岛', type: '自然景观', rating: 4.5, opening_hours: '全天开放'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (donggang_caomei:Food {name: '东港草莓', type: '地方特产', price_range: '低', description: '果肉细腻，香甜可口'}),
               (donggang_haixian:Food {name: '海鲜', type: '地方特色', price_range: '中', description: '新鲜肥美，品种丰富'}),
               (donggang_binguan:Accommodation {name: '东港宾馆', type: '三星级酒店', price_range: '中低', rating: 4.3}),
               (donggang_huanghai:Accommodation {name: '东港黄海大酒店', type: '商务酒店', price_range: '中低', rating: 4.2}),
               (donggang_bus:Transportation {name: '东港公交', type: '公交', route: '覆盖市区', price: '1-2元'}),
               (donggang_bei:Transportation {name: '东港北站', type: '高铁站', route: '通往丹东等地', price: '根据里程'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '东港'})
               WHERE a.name IN ['大鹿岛', '獐岛']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '东港'}), (f:Food)
               WHERE f.name IN ['东港草莓', '海鲜']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '大鹿岛'}), (f:Food {name: '海鲜'})
               CREATE (a)-[:NEAR_FOOD {distance: '200m', tip: '海岛渔村可品尝当日捕捞海鲜'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '大鹿岛'}), (f:Food {name: '东港草莓'})
               CREATE (a)-[:NEAR_FOOD {distance: '8km', tip: '岛外草莓种植基地可体验采摘'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '獐岛'}), (f:Food {name: '海鲜'})
               CREATE (a)-[:NEAR_FOOD {distance: '300m', tip: '海岛码头餐馆可享用现煮海产'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '大鹿岛'}), (ac:Accommodation {name: '东港宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '10km', tip: '适合海岛度假后休整，提供草莓甜品'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '獐岛'}), (ac:Accommodation {name: '东港黄海大酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '12km', tip: '靠近海岛码头，方便登岛游览行程'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '东港'}), (t:Transportation)
               WHERE t.name IN ['东港公交', '东港北站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '东港公交'}), (t2:Transportation {name: '东港北站'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '公交专线直达高铁站，方便前往丹东、沈阳等地'}]->(t2)
           """)

        print("东港旅游数据导入完成！")

    def import_fengcheng_data(self):
        """导入凤城旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (fc:City {name: '凤城', level: '县级市', description: '辽宁省县级市，丹东代管，中国硼都，满族聚居地'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (fenghuangshan:Attraction {name: '凤凰山', type: '自然景观', rating: 4.7, opening_hours: '7:30 - 16:30'}),
               (dalishu_shengtai:Attraction {name: '大梨树生态旅游区', type: '自然景观', rating: 4.5, opening_hours: '8:00 - 17:00'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (fengcheng_laojiao:Food {name: '凤城老窖', type: '地方特产', price_range: '中', description: '酒香浓郁，口感醇厚'}),
               (manzu_bobo:Food {name: '满族饽饽', type: '传统美食', price_range: '低', description: '做工精细，风味独特'}),
               (fengcheng_binguan:Accommodation {name: '凤城宾馆', type: '三星级酒店', price_range: '中低', rating: 4.3}),
               (fengcheng_guoji:Accommodation {name: '凤城国际酒店', type: '商务酒店', price_range: '中低', rating: 4.2}),
               (fengcheng_bus:Transportation {name: '凤城公交', type: '公交', route: '覆盖市区', price: '1-2元'}),
               (fengcheng_dong:Transportation {name: '凤城东站', type: '高铁站', route: '通往丹东等地', price: '根据里程'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '凤城'})
               WHERE a.name IN ['凤凰山', '大梨树生态旅游区']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '凤城'}), (f:Food)
               WHERE f.name IN ['凤城老窖', '满族饽饽']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '大梨树生态旅游区'}), (f:Food {name: '满族饽饽'})
               CREATE (a)-[:NEAR_FOOD {distance: '500m', tip: '景区民俗村可品尝现做满族饽饽'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '大梨树生态旅游区'}), (f:Food {name: '凤城老窖'})
               CREATE (a)-[:NEAR_FOOD {distance: '800m', tip: '景区酒坊可品鉴原浆凤城老窖'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '凤凰山'}), (f:Food {name: '满族饽饽'})
               CREATE (a)-[:NEAR_FOOD {distance: '2km', tip: '山脚下满族餐馆有传统饽饽供应'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '凤凰山'}), (ac:Accommodation {name: '凤城宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '3km', tip: '适合山地游览后休整，提供满族特色餐'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '大梨树生态旅游区'}), (ac:Accommodation {name: '凤城国际酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '5km', tip: '靠近生态景区，方便乡村旅游行程'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '凤城'}), (t:Transportation)
               WHERE t.name IN ['凤城公交', '凤城东站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '凤城公交'}), (t2:Transportation {name: '凤城东站'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '公交专线直达高铁站，方便前往丹东、沈阳等地'}]->(t2)
           """)

        print("凤城旅游数据导入完成！")

    def import_linghai_data(self):
        """导入凌海旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (lh:City {name: '凌海', level: '县级市', description: '辽宁省县级市，锦州代管，渤海湾畔重要城市'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (cuiyanshan:Attraction {name: '翠岩山', type: '自然景观', rating: 4.4, opening_hours: '8:00 - 17:00'}),
               (yanjingsi:Attraction {name: '岩井寺', type: '人文景观', rating: 4.3, opening_hours: '8:30 - 16:30'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (linghai_haixian:Food {name: '凌海海鲜', type: '地方特色', price_range: '中', description: '新鲜美味，品种丰富'}),
               (linghai_pingguo:Food {name: '苹果', type: '地方特产', price_range: '低', description: '脆甜多汁，品质优良'}),
               (linghai_guoji:Accommodation {name: '凌海国际酒店', type: '三星级酒店', price_range: '中低', rating: 4.3}),
               (linghai_binguan:Accommodation {name: '凌海宾馆', type: '商务酒店', price_range: '中低', rating: 4.2}),
               (linghai_bus:Transportation {name: '凌海公交', type: '公交', route: '覆盖市区', price: '1-2元'}),
               (linghai_nan:Transportation {name: '凌海南站', type: '高铁站', route: '通往锦州等地', price: '根据里程'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '凌海'})
               WHERE a.name IN ['翠岩山', '岩井寺']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '凌海'}), (f:Food)
               WHERE f.name IN ['凌海海鲜', '苹果']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '翠岩山'}), (f:Food {name: '苹果'})
               CREATE (a)-[:NEAR_FOOD {distance: '1km', tip: '山脚下果园可采摘新鲜苹果'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '翠岩山'}), (f:Food {name: '凌海海鲜'})
               CREATE (a)-[:NEAR_FOOD {distance: '5km', tip: '山下小镇海鲜馆可搭配山野菜食用'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '岩井寺'}), (f:Food {name: '凌海海鲜'})
               CREATE (a)-[:NEAR_FOOD {distance: '3km', tip: '寺庙周边渔家餐馆可品尝当日海产'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '翠岩山'}), (ac:Accommodation {name: '凌海国际酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '6km', tip: '适合山地游览后休整，提供海鲜盛宴'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '岩井寺'}), (ac:Accommodation {name: '凌海宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '4km', tip: '靠近人文景点，方便文化探访行程'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '凌海'}), (t:Transportation)
               WHERE t.name IN ['凌海公交', '凌海南站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '凌海公交'}), (t2:Transportation {name: '凌海南站'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '公交专线直达高铁站，方便前往锦州、沈阳等地'}]->(t2)
           """)

        print("凌海旅游数据导入完成！")

    def import_beizhen_data(self):
        """导入北镇旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (bz:City {name: '北镇', level: '县级市', description: '辽宁省县级市，锦州代管，中国梨都，历史文化名城'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (yiwulvshan:Attraction {name: '医巫闾山', type: '自然景观', rating: 4.7, opening_hours: '8:00 - 17:00'}),
               (beizhen_miao:Attraction {name: '北镇庙', type: '人文景观', rating: 4.5, opening_hours: '8:30 - 16:30'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (beizhen_zhuti:Food {name: '北镇猪蹄', type: '地方特色', price_range: '中低', description: '软烂入味，肥而不腻'}),
               (yali:Food {name: '鸭梨', type: '地方特产', price_range: '低', description: '汁多味甜，肉质细腻'}),
               (beizhen_dasha:Accommodation {name: '北镇大厦', type: '三星级酒店', price_range: '中低', rating: 4.3}),
               (beizhen_binguan:Accommodation {name: '北镇宾馆', type: '商务酒店', price_range: '中低', rating: 4.2}),
               (beizhen_bus:Transportation {name: '北镇公交', type: '公交', route: '覆盖市区', price: '1-2元'}),
               (beizhen_nan:Transportation {name: '北镇南站', type: '高铁站', route: '通往锦州等地', price: '根据里程'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '北镇'})
               WHERE a.name IN ['医巫闾山', '北镇庙']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '北镇'}), (f:Food)
               WHERE f.name IN ['北镇猪蹄', '鸭梨']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '医巫闾山'}), (f:Food {name: '鸭梨'})
               CREATE (a)-[:NEAR_FOOD {distance: '1.5km', tip: '山脚下梨园可采摘新鲜鸭梨'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '医巫闾山'}), (f:Food {name: '北镇猪蹄'})
               CREATE (a)-[:NEAR_FOOD {distance: '3km', tip: '景区出口餐馆可品尝真空包装猪蹄'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '北镇庙'}), (f:Food {name: '北镇猪蹄'})
               CREATE (a)-[:NEAR_FOOD {distance: '800m', tip: '庙外老字号店铺可现购热乎猪蹄'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '医巫闾山'}), (ac:Accommodation {name: '北镇大厦'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '5km', tip: '适合山水游览后休整，提供梨汁饮品'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '北镇庙'}), (ac:Accommodation {name: '北镇宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '1km', tip: '靠近历史景点，方便文化探访行程'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '北镇'}), (t:Transportation)
               WHERE t.name IN ['北镇公交', '北镇南站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '北镇公交'}), (t2:Transportation {name: '北镇南站'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '公交专线直达高铁站，方便前往锦州、沈阳等地'}]->(t2)
           """)

        print("北镇旅游数据导入完成！")

    def import_gaizhou_data(self):
        """导入盖州旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (gz:City {name: '盖州', level: '县级市', description: '辽宁省县级市，营口代管，中国书法之乡，苹果之乡'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (chishan:Attraction {name: '赤山', type: '自然景观', rating: 4.6, opening_hours: '8:00 - 17:00'}),
               (qinglongshan:Attraction {name: '青龙山', type: '自然景观', rating: 4.5, opening_hours: '全天开放'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (gaizhou_pingguo:Food {name: '盖州苹果', type: '地方特产', price_range: '低', description: '脆甜多汁，品质优良'}),
               (gaizhou_haixian:Food {name: '海鲜', type: '地方特色', price_range: '中', description: '新鲜肥美，品种丰富'}),
               (gaizhou_binguan:Accommodation {name: '盖州宾馆', type: '三星级酒店', price_range: '中低', rating: 4.3}),
               (gaizhou_shuangtaizi:Accommodation {name: '盖州双台子温泉度假村', type: '度假酒店', price_range: '中', rating: 4.4}),
               (gaizhou_bus:Transportation {name: '盖州公交', type: '公交', route: '覆盖市区', price: '1-2元'}),
               (gaizhou_xi:Transportation {name: '盖州西站', type: '高铁站', route: '通往营口等地', price: '根据里程'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '盖州'})
               WHERE a.name IN ['赤山', '青龙山']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '盖州'}), (f:Food)
               WHERE f.name IN ['盖州苹果', '海鲜']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '赤山'}), (f:Food {name: '盖州苹果'})
               CREATE (a)-[:NEAR_FOOD {distance: '2km', tip: '山脚下苹果园可体验采摘乐趣'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '赤山'}), (f:Food {name: '海鲜'})
               CREATE (a)-[:NEAR_FOOD {distance: '8km', tip: '山下滨海小镇可品尝当日海产'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '青龙山'}), (f:Food {name: '盖州苹果'})
               CREATE (a)-[:NEAR_FOOD {distance: '3km', tip: '景区周边果农直销新鲜苹果'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '赤山'}), (ac:Accommodation {name: '盖州宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '10km', tip: '适合山水游览后休整，提供苹果甜品'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '青龙山'}), (ac:Accommodation {name: '盖州双台子温泉度假村'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '5km', tip: '游览后可享温泉放松，配套海鲜餐厅'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '盖州'}), (t:Transportation)
               WHERE t.name IN ['盖州公交', '盖州西站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '盖州公交'}), (t2:Transportation {name: '盖州西站'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '公交专线直达高铁站，方便前往营口、沈阳等地'}]->(t2)
           """)

        print("盖州旅游数据导入完成！")

    def import_dashiqiao_data(self):
        """导入大石桥旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (dsq:City {name: '大石桥', level: '县级市', description: '辽宁省县级市，营口代管，中国镁都，耐火材料基地'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (mizhenshan:Attraction {name: '迷镇山', type: '自然景观', rating: 4.4, opening_hours: '全天开放'}),
               (jinniushan_yizhi:Attraction {name: '金牛山古人类遗址', type: '人文景观', rating: 4.3, opening_hours: '9:00 - 16:00'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (dashiqiao_dunyu:Food {name: '大石桥炖鱼', type: '地方特色', price_range: '中低', description: '汤汁鲜美，鱼肉鲜嫩'}),
               (nanguoli:Food {name: '南果梨', type: '地方特产', price_range: '低', description: '果肉细腻，酸甜适口'}),
               (dashiqiao_guoji:Accommodation {name: '大石桥国际酒店', type: '三星级酒店', price_range: '中低', rating: 4.3}),
               (dashiqiao_binguan:Accommodation {name: '大石桥宾馆', type: '商务酒店', price_range: '中低', rating: 4.2}),
               (dashiqiao_bus:Transportation {name: '大石桥公交', type: '公交', route: '覆盖市区', price: '1-2元'}),
               (dashiqiao_railway:Transportation {name: '大石桥站', type: '火车站', route: '通往营口等地', price: '根据里程'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '大石桥'})
               WHERE a.name IN ['迷镇山', '金牛山古人类遗址']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '大石桥'}), (f:Food)
               WHERE f.name IN ['大石桥炖鱼', '南果梨']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '迷镇山'}), (f:Food {name: '大石桥炖鱼'})
               CREATE (a)-[:NEAR_FOOD {distance: '1km', tip: '山脚下水库鱼馆可品尝现炖河鱼'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '迷镇山'}), (f:Food {name: '南果梨'})
               CREATE (a)-[:NEAR_FOOD {distance: '2km', tip: '山腰果林可采摘当季南果梨'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '金牛山古人类遗址'}), (f:Food {name: '南果梨'})
               CREATE (a)-[:NEAR_FOOD {distance: '4km', tip: '遗址周边农家有新鲜南果梨售卖'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '迷镇山'}), (ac:Accommodation {name: '大石桥国际酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '5km', tip: '适合自然游览后休整，提供炖鱼特色餐'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '金牛山古人类遗址'}), (ac:Accommodation {name: '大石桥宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '8km', tip: '靠近人文遗址，方便考古研学行程'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '大石桥'}), (t:Transportation)
               WHERE t.name IN ['大石桥公交', '大石桥站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '大石桥公交'}), (t2:Transportation {name: '大石桥站'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '公交直达火车站，方便前往营口、沈阳等地'}]->(t2)
           """)

        print("大石桥旅游数据导入完成！")

    def import_dengta_data(self):
        """导入灯塔旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (dt:City {name: '灯塔', level: '县级市', description: '辽宁省县级市，辽阳代管，中国皮装裘皮基地'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (gex西河:Attraction {name: '葛西河生态走廊', type: '自然景观', rating: 4.3, opening_hours: '全天开放'}),
               (yanzhoucheng:Attraction {name: '燕州城遗址', type: '人文景观', rating: 4.2, opening_hours: '9:00 - 16:00'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (dengta_dami:Food {name: '灯塔大米', type: '地方特产', price_range: '低', description: '米粒饱满，口感香糯'}),
               (pidong:Food {name: '皮冻', type: '传统美食', price_range: '低', description: '晶莹剔透，口感爽滑'}),
               (dengta_binguan:Accommodation {name: '灯塔宾馆', type: '三星级酒店', price_range: '中低', rating: 4.2}),
               (dengta_jinhui:Accommodation {name: '灯塔金汇酒店', type: '商务酒店', price_range: '中低', rating: 4.1}),
               (dengta_bus:Transportation {name: '灯塔公交', type: '公交', route: '覆盖市区', price: '1-2元'}),
               (dengta_railway:Transportation {name: '灯塔站', type: '火车站', route: '通往辽阳等地', price: '根据里程'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '灯塔'})
               WHERE a.name IN ['葛西河生态走廊', '燕州城遗址']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '灯塔'}), (f:Food)
               WHERE f.name IN ['灯塔大米', '皮冻']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '葛西河生态走廊'}), (f:Food {name: '灯塔大米'})
               CREATE (a)-[:NEAR_FOOD {distance: '800m', tip: '河畔农家餐馆可用新米制作米饭'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '葛西河生态走廊'}), (f:Food {name: '皮冻'})
               CREATE (a)-[:NEAR_FOOD {distance: '500m', tip: '走廊周边熟食店有特色皮冻售卖'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '燕州城遗址'}), (f:Food {name: '皮冻'})
               CREATE (a)-[:NEAR_FOOD {distance: '3km', tip: '遗址山下餐馆可搭配皮冻品尝农家菜'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '葛西河生态走廊'}), (ac:Accommodation {name: '灯塔宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '2km', tip: '适合生态休闲后休整，提供大米主食'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '燕州城遗址'}), (ac:Accommodation {name: '灯塔金汇酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '6km', tip: '靠近历史遗址，方便文化探访行程'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '灯塔'}), (t:Transportation)
               WHERE t.name IN ['灯塔公交', '灯塔站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '灯塔公交'}), (t2:Transportation {name: '灯塔站'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '公交直达火车站，方便前往辽阳、沈阳等地'}]->(t2)
           """)

        print("灯塔旅游数据导入完成！")

    def import_diaobingshan_data(self):
        """导入调兵山旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (dbs:City {name: '调兵山', level: '县级市', description: '辽宁省县级市，铁岭代管，中国煤电能源基地'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (mingyue_chansi:Attraction {name: '明月禅寺', type: '人文景观', rating: 4.4, opening_hours: '8:30 - 16:30'}),
               (bingshan_guangchang:Attraction {name: '兵山广场', type: '人文景观', rating: 4.3, opening_hours: '全天开放'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (diaobingshan_xunrou:Food {name: '调兵山熏肉大饼', type: '地方小吃', price_range: '低', description: '熏香浓郁，饼皮酥脆'}),
               (meikuang_hefan:Food {name: '煤矿工人盒饭', type: '地方特色', price_range: '低', description: '分量足，味道鲜美'}),
               (diaobingshan_meidu:Accommodation {name: '调兵山煤都宾馆', type: '三星级酒店', price_range: '中低', rating: 4.3}),
               (diaobingshan_binguan:Accommodation {name: '调兵山宾馆', type: '商务酒店', price_range: '中低', rating: 4.2}),
               (diaobingshan_bus:Transportation {name: '调兵山公交', type: '公交', route: '覆盖市区', price: '1-2元'}),
               (diaobingshan_railway:Transportation {name: '调兵山站', type: '火车站', route: '通往铁岭等地', price: '根据里程'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '调兵山'})
               WHERE a.name IN ['明月禅寺', '兵山广场']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '调兵山'}), (f:Food)
               WHERE f.name IN ['调兵山熏肉大饼', '煤矿工人盒饭']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '兵山广场'}), (f:Food {name: '调兵山熏肉大饼'})
               CREATE (a)-[:NEAR_FOOD {distance: '300m', tip: '广场周边老字号店铺可现做熏肉大饼'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '兵山广场'}), (f:Food {name: '煤矿工人盒饭'})
               CREATE (a)-[:NEAR_FOOD {distance: '500m', tip: '广场美食街可体验复古工人盒饭'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '明月禅寺'}), (f:Food {name: '调兵山熏肉大饼'})
               CREATE (a)-[:NEAR_FOOD {distance: '2km', tip: '寺庙外素食馆有素馅版大饼供应'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '明月禅寺'}), (ac:Accommodation {name: '调兵山煤都宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '3km', tip: '适合文化探访后休整，提供特色熏肉早餐'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '兵山广场'}), (ac:Accommodation {name: '调兵山宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '800m', tip: '靠近城市广场，方便体验市井生活'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '调兵山'}), (t:Transportation)
               WHERE t.name IN ['调兵山公交', '调兵山站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '调兵山公交'}), (t2:Transportation {name: '调兵山站'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '公交直达火车站，方便前往铁岭、沈阳等地'}]->(t2)
           """)

        print("调兵山旅游数据导入完成！")

    def import_kaiyuan_data(self):
        """导入开原旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (ky:City {name: '开原', level: '县级市', description: '辽宁省县级市，铁岭代管，中国大蒜之乡'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (xianzhou_gucheng:Attraction {name: '咸州古城', type: '人文景观', rating: 4.4, opening_hours: '8:30 - 16:30'}),
               (xiangyashan:Attraction {name: '象牙山', type: '自然景观', rating: 4.3, opening_hours: '全天开放'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (kaiyuan_dasuan:Food {name: '开原大蒜', type: '地方特产', price_range: '低', description: '蒜香浓郁，品质优良'}),
               (huoshao:Food {name: '火勺', type: '地方小吃', price_range: '低', description: '外酥里嫩，馅料丰富'}),
               (kaiyuan_guoji:Accommodation {name: '开原国际酒店', type: '三星级酒店', price_range: '中低', rating: 4.3}),
               (kaiyuan_binguan:Accommodation {name: '开原宾馆', type: '商务酒店', price_range: '中低', rating: 4.2}),
               (kaiyuan_bus:Transportation {name: '开原公交', type: '公交', route: '覆盖市区', price: '1-2元'}),
               (kaiyuan_xi:Transportation {name: '开原西站', type: '高铁站', route: '通往铁岭等地', price: '根据里程'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '开原'})
               WHERE a.name IN ['咸州古城', '象牙山']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '开原'}), (f:Food)
               WHERE f.name IN ['开原大蒜', '火勺']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '咸州古城'}), (f:Food {name: '开原大蒜'})
               CREATE (a)-[:NEAR_FOOD {distance: '400m', tip: '古城农贸市场可选购优质大蒜及加工制品'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '咸州古城'}), (f:Food {name: '火勺'})
               CREATE (a)-[:NEAR_FOOD {distance: '200m', tip: '古城墙下老字号火勺店可现烤现吃'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '象牙山'}), (f:Food {name: '火勺'})
               CREATE (a)-[:NEAR_FOOD {distance: '3km', tip: '山脚下农家餐馆用火勺搭配山野菜食用'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '咸州古城'}), (ac:Accommodation {name: '开原国际酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '1km', tip: '适合历史文化探访后休整，提供大蒜风味菜肴'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '象牙山'}), (ac:Accommodation {name: '开原宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '5km', tip: '靠近自然景区，方便山地游览行程'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '开原'}), (t:Transportation)
               WHERE t.name IN ['开原公交', '开原西站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '开原公交'}), (t2:Transportation {name: '开原西站'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '公交专线直达高铁站，方便前往铁岭、沈阳等地'}]->(t2)
           """)

        print("开原旅游数据导入完成！")

    def import_beipiao_data(self):
        """导入北票旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (bp:City {name: '北票', level: '县级市', description: '辽宁省县级市，朝阳代管，中国化石之乡，古生物王国'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (niaohuashi_gongyuan:Attraction {name: '鸟化石国家地质公园', type: '自然景观', rating: 4.6, opening_hours: '9:00 - 16:30'}),
               (daheishan_gongyuan:Attraction {name: '大黑山国家森林公园', type: '自然景观', rating: 4.5, opening_hours: '8:00 - 17:00'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (beipiao_yangtang:Food {name: '北票羊汤', type: '地方特色', price_range: '中低', description: '汤鲜味美，暖胃驱寒'}),
               (beipiao_xiaomi:Food {name: '小米', type: '地方特产', price_range: '低', description: '米香浓郁，营养丰富'}),
               (beipiao_guoji:Accommodation {name: '北票国际酒店', type: '三星级酒店', price_range: '中低', rating: 4.3}),
               (beipiao_binguan:Accommodation {name: '北票宾馆', type: '商务酒店', price_range: '中低', rating: 4.2}),
               (beipiao_bus:Transportation {name: '北票公交', type: '公交', route: '覆盖市区', price: '1-2元'}),
               (beipiao_railway:Transportation {name: '北票站', type: '火车站', route: '通往朝阳等地', price: '根据里程'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '北票'})
               WHERE a.name IN ['鸟化石国家地质公园', '大黑山国家森林公园']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '北票'}), (f:Food)
               WHERE f.name IN ['北票羊汤', '小米']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '大黑山国家森林公园'}), (f:Food {name: '北票羊汤'})
               CREATE (a)-[:NEAR_FOOD {distance: '2km', tip: '森林公园出口处农家乐可品尝现熬羊汤'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '大黑山国家森林公园'}), (f:Food {name: '小米'})
               CREATE (a)-[:NEAR_FOOD {distance: '4km', tip: '山脚下农户可购买新磨小米及小米制品'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '鸟化石国家地质公园'}), (f:Food {name: '小米'})
               CREATE (a)-[:NEAR_FOOD {distance: '3km', tip: '景区周边特产店有真空包装小米出售'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '大黑山国家森林公园'}), (ac:Accommodation {name: '北票国际酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '8km', tip: '适合自然游览后休整，提供羊汤早餐'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '鸟化石国家地质公园'}), (ac:Accommodation {name: '北票宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '5km', tip: '靠近地质公园，方便化石科考行程'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '北票'}), (t:Transportation)
               WHERE t.name IN ['北票公交', '北票站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '北票公交'}), (t2:Transportation {name: '北票站'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '公交直达火车站，方便前往朝阳、沈阳等地'}]->(t2)
           """)

        print("北票旅游数据导入完成！")

    def import_lingyuan_data(self):
        """导入凌源旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (ly:City {name: '凌源', level: '县级市', description: '辽宁省县级市，朝阳代管，中国百合之乡，辽西古城'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (reshuitang_wenquan:Attraction {name: '热水汤温泉', type: '自然景观', rating: 4.5, opening_hours: '全天开放'}),
               (tianshenghao_shiku:Attraction {name: '天盛号石窟', type: '人文景观', rating: 4.4, opening_hours: '9:00 - 16:30'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (lingyuan_baihe:Food {name: '凌源百合', type: '地方特产', price_range: '中低', description: '花瓣肥厚，品质优良'}),
               (bomian:Food {name: '拨面', type: '地方小吃', price_range: '低', description: '面条筋道，卤汁鲜美'}),
               (lingyuan_guoji:Accommodation {name: '凌源国际酒店', type: '三星级酒店', price_range: '中低', rating: 4.3}),
               (lingyuan_binguan:Accommodation {name: '凌源宾馆', type: '商务酒店', price_range: '中低', rating: 4.2}),
               (lingyuan_bus:Transportation {name: '凌源公交', type: '公交', route: '覆盖市区', price: '1-2元'}),
               (lingyuan_railway:Transportation {name: '凌源站', type: '火车站', route: '通往朝阳等地', price: '根据里程'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '凌源'})
               WHERE a.name IN ['热水汤温泉', '天盛号石窟']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '凌源'}), (f:Food)
               WHERE f.name IN ['凌源百合', '拨面']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '热水汤温泉'}), (f:Food {name: '凌源百合'})
               CREATE (a)-[:NEAR_FOOD {distance: '1.5km', tip: '温泉度假区内花店可购新鲜百合，餐厅有百合甜品'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '热水汤温泉'}), (f:Food {name: '拨面'})
               CREATE (a)-[:NEAR_FOOD {distance: '800m', tip: '温泉周边餐馆可品尝现做拨面，搭配本地卤料'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '天盛号石窟'}), (f:Food {name: '拨面'})
               CREATE (a)-[:NEAR_FOOD {distance: '3km', tip: '石窟山下村落有传统拨面手艺店'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '热水汤温泉'}), (ac:Accommodation {name: '凌源国际酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '2km', tip: '温泉养生后可便捷休整，提供百合炖品'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '天盛号石窟'}), (ac:Accommodation {name: '凌源宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '5km', tip: '靠近人文景点，方便石窟文化探访行程'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '凌源'}), (t:Transportation)
               WHERE t.name IN ['凌源公交', '凌源站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '凌源公交'}), (t2:Transportation {name: '凌源站'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '公交直达火车站，方便前往朝阳、承德等地'}]->(t2)
           """)

        print("凌源旅游数据导入完成！")

    def import_xingcheng_data(self):
        """导入兴城旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (xc:City {name: '兴城', level: '县级市', description: '辽宁省县级市，葫芦岛代管，中国温泉之城，历史文化名城'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (xingcheng_gucheng:Attraction {name: '兴城古城', type: '人文景观', rating: 4.7, opening_hours: '8:30 - 17:00'}),
               (xingcheng_haibin:Attraction {name: '兴城海滨', type: '自然景观', rating: 4.6, opening_hours: '全天开放'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (xingcheng_haixian:Food {name: '海鲜', type: '地方特色', price_range: '中', description: '新鲜肥美，品种丰富'}),
               (xingcheng_quanyangyan:Food {name: '兴城全羊宴', type: '地方特色', price_range: '中高', description: '肉质鲜嫩，风味独特'}),
               (xingcheng_wenquan:Accommodation {name: '兴城温泉酒店', type: '四星级酒店', price_range: '中', rating: 4.5}),
               (xingcheng_binguan:Accommodation {name: '兴城宾馆', type: '商务酒店', price_range: '中低', rating: 4.3}),
               (xingcheng_bus:Transportation {name: '兴城公交', type: '公交', route: '覆盖市区', price: '1-2元'}),
               (xingcheng_xi:Transportation {name: '兴城西站', type: '高铁站', route: '通往葫芦岛等地', price: '根据里程'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '兴城'})
               WHERE a.name IN ['兴城古城', '兴城海滨']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '兴城'}), (f:Food)
               WHERE f.name IN ['海鲜', '兴城全羊宴']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '兴城海滨'}), (f:Food {name: '海鲜'})
               CREATE (a)-[:NEAR_FOOD {distance: '300m', tip: '海滨浴场周边海鲜排档可品尝当日捕捞海产'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '兴城海滨'}), (f:Food {name: '兴城全羊宴'})
               CREATE (a)-[:NEAR_FOOD {distance: '2km', tip: '海滨度假村内餐馆可享全羊宴搭配海鲜'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '兴城古城'}), (f:Food {name: '兴城全羊宴'})
               CREATE (a)-[:NEAR_FOOD {distance: '1km', tip: '古城内老字号餐馆可体验传统全羊宴'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '兴城海滨'}), (ac:Accommodation {name: '兴城温泉酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '3km', tip: '海滨游玩后可享温泉放松，配套海鲜餐厅'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '兴城古城'}), (ac:Accommodation {name: '兴城宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '800m', tip: '靠近历史古城，方便文化探访行程'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '兴城'}), (t:Transportation)
               WHERE t.name IN ['兴城公交', '兴城西站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '兴城公交'}), (t2:Transportation {name: '兴城西站'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '公交专线直达高铁站，方便前往葫芦岛、锦州等地'}]->(t2)
           """)

        print("兴城旅游数据导入完成！")

    def import_changchun_data(self):
        """导入长春旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (cc:City {name: '长春', level: '地级市', description: '吉林省省会，中国汽车工业摇篮，北国春城'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (weiman_huanggong:Attraction {name: '伪满皇宫博物院', type: '人文景观', rating: 4.7, opening_hours: '8:30 - 17:00'}),
               (jingyuetan_gongyuan:Attraction {name: '净月潭国家森林公园', type: '自然景观', rating: 4.8, opening_hours: '8:00 - 17:00'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (guobaorou:Food {name: '锅包肉', type: '吉菜', price_range: '中低', description: '外酥里嫩，酸甜可口'}),
               (changchun_jiangrou:Food {name: '长春酱肉', type: '地方特色', price_range: '中低', description: '酱香浓郁，肥而不腻'}),
               (changchun_xianggelila:Accommodation {name: '长春香格里拉大酒店', type: '五星级酒店', price_range: '高', rating: 4.7}),
               (changchun_kaiyue:Accommodation {name: '长春凯悦酒店', type: '五星级酒店', price_range: '高', rating: 4.6}),
               (changchun_metro3:Transportation {name: '长春轨道交通3号线', type: '地铁', route: '长春站-长影世纪城', price: '2-6元'}),
               (longjia_dabache:Transportation {name: '龙嘉机场大巴', type: '机场巴士', route: '市区-龙嘉机场', price: '20元'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '长春'})
               WHERE a.name IN ['伪满皇宫博物院', '净月潭国家森林公园']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '长春'}), (f:Food)
               WHERE f.name IN ['锅包肉', '长春酱肉']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '伪满皇宫博物院'}), (f:Food {name: '锅包肉'})
               CREATE (a)-[:NEAR_FOOD {distance: '500m', tip: '博物院周边老字号吉菜馆可品尝地道锅包肉'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '伪满皇宫博物院'}), (f:Food {name: '长春酱肉'})
               CREATE (a)-[:NEAR_FOOD {distance: '800m', tip: '景区附近熟食店可购真空包装酱肉'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '净月潭国家森林公园'}), (f:Food {name: '锅包肉'})
               CREATE (a)-[:NEAR_FOOD {distance: '3km', tip: '潭边度假酒店餐厅可享锅包肉配山野菜'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '伪满皇宫博物院'}), (ac:Accommodation {name: '长春香格里拉大酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '2km', tip: '适合历史文化探访后休整，提供吉菜套餐'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '净月潭国家森林公园'}), (ac:Accommodation {name: '长春凯悦酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '5km', tip: '靠近自然景区，方便森林游览行程'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '长春'}), (t:Transportation)
               WHERE t.name IN ['长春轨道交通3号线', '龙嘉机场大巴']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '长春轨道交通3号线'}), (t2:Transportation {name: '龙嘉机场大巴'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '地铁3号线长春站站可换乘机场大巴，直达龙嘉国际机场'}]->(t2)
           """)

        print("长春旅游数据导入完成！")

    def import_jilin_data(self):
        """导入吉林市旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (jl:City {name: '吉林', level: '地级市', description: '吉林省地级市，北国江城，中国化工城'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (wusongdao:Attraction {name: '雾凇岛', type: '自然景观', rating: 4.7, opening_hours: '全天开放'}),
               (beishan_gongyuan:Attraction {name: '北山公园', type: '人文景观', rating: 4.5, opening_hours: '8:00 - 17:00'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (bairou_xuechang:Food {name: '白肉血肠', type: '地方特色', price_range: '中低', description: '肉质鲜嫩，血肠爽滑'}),
               (qingling_huoyu:Food {name: '庆岭活鱼', type: '地方特色', price_range: '中', description: '鱼肉鲜嫩，汤汁浓郁'}),
               (jilin_shimao:Accommodation {name: '吉林世贸万锦大酒店', type: '五星级酒店', price_range: '高', rating: 4.6}),
               (jilin_shiji:Accommodation {name: '吉林世纪大饭店', type: '五星级酒店', price_range: '高', rating: 4.5}),
               (jilin_bus:Transportation {name: '吉林公交', type: '公交', route: '覆盖市区', price: '1-2元'}),
               (jilin_railway:Transportation {name: '吉林站', type: '高铁站', route: '通往长春等地', price: '根据里程'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '吉林'})
               WHERE a.name IN ['雾凇岛', '北山公园']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '吉林'}), (f:Food)
               WHERE f.name IN ['白肉血肠', '庆岭活鱼']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '雾凇岛'}), (f:Food {name: '白肉血肠'})
               CREATE (a)-[:NEAR_FOOD {distance: '1km', tip: '岛上农家餐馆可品尝现做白肉血肠，配酸菜锅底'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '雾凇岛'}), (f:Food {name: '庆岭活鱼'})
               CREATE (a)-[:NEAR_FOOD {distance: '3km', tip: '岛外松花江畔鱼馆可享现捕活鱼炖制'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '北山公园'}), (f:Food {name: '白肉血肠'})
               CREATE (a)-[:NEAR_FOOD {distance: '800m', tip: '公园南门老字号餐馆有传统做法白肉血肠'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '雾凇岛'}), (ac:Accommodation {name: '吉林世贸万锦大酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '15km', tip: '雾凇观赏后可享舒适住宿，提供东北特色晚餐'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '北山公园'}), (ac:Accommodation {name: '吉林世纪大饭店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '2km', tip: '靠近人文景点，方便文化游览行程'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '吉林'}), (t:Transportation)
               WHERE t.name IN ['吉林公交', '吉林站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '吉林公交'}), (t2:Transportation {name: '吉林站'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '多条公交线直达吉林站，方便前往长春、哈尔滨等地'}]->(t2)
           """)

        print("吉林市旅游数据导入完成！")

    def import_siping_data(self):
        """导入四平旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (sp:City {name: '四平', level: '地级市', description: '吉林省地级市，英雄城，东北军事重镇'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (yehenala_cheng:Attraction {name: '叶赫那拉城', type: '人文景观', rating: 4.5, opening_hours: '8:30 - 16:30'}),
               (siping_zhanyi:Attraction {name: '四平战役纪念馆', type: '人文景观', rating: 4.6, opening_hours: '9:00 - 16:00'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (liliangui_xunrou:Food {name: '李连贵熏肉大饼', type: '地方特色', price_range: '中低', description: '熏香浓郁，饼皮酥脆'}),
               (yitong_shaogezi:Food {name: '伊通烧鸽子', type: '地方特色', price_range: '中', description: '肉质鲜嫩，香味扑鼻'}),
               (siping_wanda:Accommodation {name: '四平富力万达嘉华酒店', type: '五星级酒店', price_range: '高', rating: 4.5}),
               (siping_binguan:Accommodation {name: '四平宾馆', type: '四星级酒店', price_range: '中', rating: 4.3}),
               (siping_bus:Transportation {name: '四平公交', type: '公交', route: '覆盖市区', price: '1-2元'}),
               (siping_dong:Transportation {name: '四平东站', type: '高铁站', route: '通往长春等地', price: '根据里程'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '四平'})
               WHERE a.name IN ['叶赫那拉城', '四平战役纪念馆']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '四平'}), (f:Food)
               WHERE f.name IN ['李连贵熏肉大饼', '伊通烧鸽子']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '叶赫那拉城'}), (f:Food {name: '李连贵熏肉大饼'})
               CREATE (a)-[:NEAR_FOOD {distance: '500m', tip: '城内满族餐馆可品尝熏肉大饼配满族小菜'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '叶赫那拉城'}), (f:Food {name: '伊通烧鸽子'})
               CREATE (a)-[:NEAR_FOOD {distance: '800m', tip: '城外烧烤街可享现烤鸽子，配特色蘸料'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '四平战役纪念馆'}), (f:Food {name: '李连贵熏肉大饼'})
               CREATE (a)-[:NEAR_FOOD {distance: '1km', tip: '纪念馆周边分店可体验经典熏肉大饼'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '叶赫那拉城'}), (ac:Accommodation {name: '四平富力万达嘉华酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '30km', tip: '适合满族文化探访后休整，提供特色餐饮'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '四平战役纪念馆'}), (ac:Accommodation {name: '四平宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '1.5km', tip: '靠近红色景点，方便历史研学行程'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '四平'}), (t:Transportation)
               WHERE t.name IN ['四平公交', '四平东站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '四平公交'}), (t2:Transportation {name: '四平东站'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '公交专线直达高铁站，方便前往长春、沈阳等地'}]->(t2)
           """)

        print("四平旅游数据导入完成！")

    def import_liaoyuan_data(self):
        """导入辽源旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (ly:City {name: '辽源', level: '地级市', description: '吉林省地级市，中国梅花鹿之乡，中国袜业名城'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (longshan_gongyuan:Attraction {name: '龙山公园', type: '自然景观', rating: 4.4, opening_hours: '全天开放'}),
               (kuanggongmu_chenlieguan:Attraction {name: '矿工墓陈列馆', type: '人文景观', rating: 4.5, opening_hours: '9:00 - 16:00'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (liaoyuan_lurou:Food {name: '辽源鹿肉', type: '地方特色', price_range: '中', description: '肉质鲜嫩，营养丰富'}),
               (guandong_zhengjiao:Food {name: '关东蒸饺', type: '地方小吃', price_range: '低', description: '皮薄馅大，汤汁鲜美'}),
               (liaoyuan_binguan:Accommodation {name: '辽源宾馆', type: '四星级酒店', price_range: '中', rating: 4.4}),
               (liaoyuan_dongfang:Accommodation {name: '辽源东方宾馆', type: '商务酒店', price_range: '中低', rating: 4.2}),
               (liaoyuan_bus:Transportation {name: '辽源公交', type: '公交', route: '覆盖市区', price: '1-2元'}),
               (liaoyuan_railway:Transportation {name: '辽源站', type: '火车站', route: '通往长春等地', price: '根据里程'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '辽源'})
               WHERE a.name IN ['龙山公园', '矿工墓陈列馆']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '辽源'}), (f:Food)
               WHERE f.name IN ['辽源鹿肉', '关东蒸饺']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '龙山公园'}), (f:Food {name: '辽源鹿肉'})
               CREATE (a)-[:NEAR_FOOD {distance: '600m', tip: '公园北门餐馆可品尝鹿肉火锅及鹿肉烧烤'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '龙山公园'}), (f:Food {name: '关东蒸饺'})
               CREATE (a)-[:NEAR_FOOD {distance: '300m', tip: '公园南门小吃街可享现蒸关东蒸饺'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '矿工墓陈列馆'}), (f:Food {name: '关东蒸饺'})
               CREATE (a)-[:NEAR_FOOD {distance: '1.2km', tip: '陈列馆周边餐馆有用传统工艺制作的蒸饺'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '龙山公园'}), (ac:Accommodation {name: '辽源宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '1km', tip: '适合城市景观游览后休整，提供鹿肉特色菜'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '矿工墓陈列馆'}), (ac:Accommodation {name: '辽源东方宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '2km', tip: '靠近历史场馆，方便红色研学行程'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '辽源'}), (t:Transportation)
               WHERE t.name IN ['辽源公交', '辽源站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '辽源公交'}), (t2:Transportation {name: '辽源站'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '公交直达火车站，方便前往长春、沈阳等地'}]->(t2)
           """)

        print("辽源旅游数据导入完成！")

    def import_tonghua_data(self):
        """导入通化旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (th:City {name: '通化', level: '地级市', description: '吉林省地级市，中国葡萄酒城，北国山城'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (jingyu_lingyuan:Attraction {name: '靖宇陵园', type: '人文景观', rating: 4.6, opening_hours: '8:30 - 16:30'}),
               (wunvfeng_gongyuan:Attraction {name: '五女峰国家森林公园', type: '自然景观', rating: 4.7, opening_hours: '8:00 - 17:00'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (tonghua_putaojiu:Food {name: '通化葡萄酒', type: '地方特产', price_range: '中', description: '酒香浓郁，口感醇厚'}),
               (gaoli_huopen:Food {name: '高丽火盆', type: '地方特色', price_range: '中', description: '配料丰富，风味独特'}),
               (tonghua_binguan:Accommodation {name: '通化宾馆', type: '四星级酒店', price_range: '中', rating: 4.5}),
               (tonghua_wantong:Accommodation {name: '通化万通大酒店', type: '商务酒店', price_range: '中低', rating: 4.3}),
               (tonghua_bus:Transportation {name: '通化公交', type: '公交', route: '覆盖市区', price: '1-2元'}),
               (tonghua_railway:Transportation {name: '通化站', type: '火车站', route: '通往长春等地', price: '根据里程'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '通化'})
               WHERE a.name IN ['靖宇陵园', '五女峰国家森林公园']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '通化'}), (f:Food)
               WHERE f.name IN ['通化葡萄酒', '高丽火盆']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '五女峰国家森林公园'}), (f:Food {name: '通化葡萄酒'})
               CREATE (a)-[:NEAR_FOOD {distance: '5km', tip: '森林公园出口酒庄可品鉴并购买通化葡萄酒'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '五女峰国家森林公园'}), (f:Food {name: '高丽火盆'})
               CREATE (a)-[:NEAR_FOOD {distance: '3km', tip: '山脚下朝鲜族餐馆可享高丽火盆配山野菜'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '靖宇陵园'}), (f:Food {name: '通化葡萄酒'})
               CREATE (a)-[:NEAR_FOOD {distance: '1.5km', tip: '陵园周边特产店有多种通化葡萄酒出售'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '五女峰国家森林公园'}), (ac:Accommodation {name: '通化宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '20km', tip: '自然游览后可舒适休整，提供葡萄酒晚宴'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '靖宇陵园'}), (ac:Accommodation {name: '通化万通大酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '1km', tip: '靠近红色景点，方便革命历史学习行程'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '通化'}), (t:Transportation)
               WHERE t.name IN ['通化公交', '通化站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '通化公交'}), (t2:Transportation {name: '通化站'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '公交直达火车站，方便前往长春、白山等地'}]->(t2)
           """)

        print("通化旅游数据导入完成！")

    def import_baishan_data(self):
        """导入白山旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (bs:City {name: '白山', level: '地级市', description: '吉林省地级市，立体资源宝库，东北生态屏障'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (changbaishan_dujiaqu:Attraction {name: '长白山国际度假区', type: '自然景观', rating: 4.8, opening_hours: '全天开放'}),
               (jinjiang_daxiagu:Attraction {name: '锦江大峡谷', type: '自然景观', rating: 4.7, opening_hours: '8:00-17:00'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (yeshanjun_yan:Food {name: '野山菌宴', type: '地方特色', price_range: '中高', description: '山珍野味，营养丰富'}),
               (linwayou:Food {name: '林蛙油', type: '地方特产', price_range: '高', description: '滋补佳品，口感独特'}),
               (changbaishan_westin:Accommodation {name: '长白山万达威斯汀度假酒店', type: '五星级', price_range: '高', rating: 4.7}),
               (baishan_binguan:Accommodation {name: '白山宾馆', type: '四星级', price_range: '中', rating: 4.3}),
               (baishan_bus:Transportation {name: '白山公交', type: '公交', route: '覆盖市区', price: '1-2元'}),
               (changbaishan_jichang:Transportation {name: '长白山机场', type: '飞机', route: '通往国内主要城市', price: '根据航线'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '白山'})
               WHERE a.name IN ['长白山国际度假区', '锦江大峡谷']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '白山'}), (f:Food)
               WHERE f.name IN ['野山菌宴', '林蛙油']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '长白山国际度假区'}), (f:Food {name: '野山菌宴'})
               CREATE (a)-[:NEAR_FOOD {distance: '1.5km', tip: '度假区内酒店可提供现采山菌制作的宴席'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '长白山国际度假区'}), (f:Food {name: '林蛙油'})
               CREATE (a)-[:NEAR_FOOD {distance: '2km', tip: '度假区特产店有精装林蛙油及即食制品'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '锦江大峡谷'}), (f:Food {name: '野山菌宴'})
               CREATE (a)-[:NEAR_FOOD {distance: '5km', tip: '峡谷出口农家乐可品尝山菌火锅'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '长白山国际度假区'}), (ac:Accommodation {name: '长白山万达威斯汀度假酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '800m', tip: '滑雪温泉后可直接入住，提供山珍特色餐'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '锦江大峡谷'}), (ac:Accommodation {name: '白山宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '30km', tip: '峡谷游览后可休整，提供林蛙油滋补餐'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '白山'}), (t:Transportation)
               WHERE t.name IN ['白山公交', '长白山机场']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '白山公交'}), (t2:Transportation {name: '长白山机场'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '公交机场专线直达长白山机场，方便前往全国主要城市'}]->(t2)
           """)

        print("白山旅游数据导入完成！")

    def import_songyuan_data(self):
        """导入松原旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (sy:City {name: '松原', level: '地级市', description: '吉林省地级市，粮仓、肉库、鱼乡，草原新城'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (chaganhu:Attraction {name: '查干湖', type: '自然景观', rating: 4.7, opening_hours: '全天开放'}),
               (longhua_si:Attraction {name: '龙华寺', type: '人文景观', rating: 4.5, opening_hours: '8:00-17:00'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (quanyu_yan:Food {name: '全鱼宴', type: '地方特色', price_range: '中高', description: '鲜嫩肥美，做法多样'}),
               (shoubariu:Food {name: '手把肉', type: '蒙餐', price_range: '中', description: '原汁原味，肉质鲜嫩'}),
               (songyuan_binguan:Accommodation {name: '松原宾馆', type: '四星级', price_range: '中', rating: 4.4}),
               (chaganhu_binguan:Accommodation {name: '查干湖宾馆', type: '特色酒店', price_range: '中', rating: 4.5}),
               (songyuan_bus:Transportation {name: '松原公交', type: '公交', route: '覆盖市区', price: '1-2元'}),
               (songyuan_railway:Transportation {name: '松原站', type: '火车', route: '通往长春等地', price: '根据里程'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '松原'})
               WHERE a.name IN ['查干湖', '龙华寺']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '松原'}), (f:Food)
               WHERE f.name IN ['全鱼宴', '手把肉']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '查干湖'}), (f:Food {name: '全鱼宴'})
               CREATE (a)-[:NEAR_FOOD {distance: '1km', tip: '湖边渔家乐可品尝当日冬捕湖鱼制作的全鱼宴'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '查干湖'}), (f:Food {name: '手把肉'})
               CREATE (a)-[:NEAR_FOOD {distance: '3km', tip: '湖畔蒙古包餐厅可享手把肉配奶茶'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '龙华寺'}), (f:Food {name: '手把肉'})
               CREATE (a)-[:NEAR_FOOD {distance: '2km', tip: '寺庙周边蒙餐馆有传统手把肉'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '查干湖'}), (ac:Accommodation {name: '查干湖宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '1.5km', tip: '适合冬捕观赏后休整，提供全鱼宴晚餐'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '龙华寺'}), (ac:Accommodation {name: '松原宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '5km', tip: '靠近宗教景点，方便文化探访行程'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '松原'}), (t:Transportation)
               WHERE t.name IN ['松原公交', '松原站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '松原公交'}), (t2:Transportation {name: '松原站'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '公交直达火车站，方便前往长春、哈尔滨等地'}]->(t2)
           """)

        print("松原旅游数据导入完成！")

    def import_baicheng_data(self):
        """导入白城旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (bc:City {name: '白城', level: '地级市', description: '吉林省地级市，鹤乡，草原湿地之城'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (xianghai_baohuqu:Attraction {name: '向海国家级自然保护区', type: '自然景观', rating: 4.7, opening_hours: '8:00-17:00'}),
               (momoge_baohuqu:Attraction {name: '莫莫格国家级自然保护区', type: '自然景观', rating: 4.6, opening_hours: '8:00-17:00'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (xianghai_yuyan:Food {name: '向海鱼宴', type: '地方特色', price_range: '中', description: '野生湖鱼，鲜美异常'}),
               (caoyuan_yangrou:Food {name: '草原羊肉', type: '地方特色', price_range: '中', description: '肉质鲜嫩，无膻味'}),
               (baicheng_binguan:Accommodation {name: '白城宾馆', type: '四星级', price_range: '中', rating: 4.4}),
               (baicheng_jihe:Accommodation {name: '白城吉鹤宾馆', type: '商务酒店', price_range: '中低', rating: 4.2}),
               (baicheng_bus:Transportation {name: '白城公交', type: '公交', route: '覆盖市区', price: '1-2元'}),
               (baicheng_railway:Transportation {name: '白城站', type: '火车', route: '通往长春等地', price: '根据里程'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '白城'})
               WHERE a.name IN ['向海国家级自然保护区', '莫莫格国家级自然保护区']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '白城'}), (f:Food)
               WHERE f.name IN ['向海鱼宴', '草原羊肉']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '向海国家级自然保护区'}), (f:Food {name: '向海鱼宴'})
               CREATE (a)-[:NEAR_FOOD {distance: '1.2km', tip: '保护区内渔家乐可品尝现捕野生湖鱼制作的鱼宴'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '向海国家级自然保护区'}), (f:Food {name: '草原羊肉'})
               CREATE (a)-[:NEAR_FOOD {distance: '3km', tip: '保护区周边草原蒙古包可享现烤羊肉'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '莫莫格国家级自然保护区'}), (f:Food {name: '向海鱼宴'})
               CREATE (a)-[:NEAR_FOOD {distance: '5km', tip: '保护区外湿地餐馆有用莫莫格湖鱼制作的鱼宴'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '向海国家级自然保护区'}), (ac:Accommodation {name: '白城宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '40km', tip: '观鹤后可舒适休整，提供鱼宴特色餐'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '莫莫格国家级自然保护区'}), (ac:Accommodation {name: '白城吉鹤宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '35km', tip: '湿地游览后可休整，提供草原羊肉菜品'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '白城'}), (t:Transportation)
               WHERE t.name IN ['白城公交', '白城站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '白城公交'}), (t2:Transportation {name: '白城站'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '公交直达火车站，方便前往长春、松原等地'}]->(t2)
           """)

        print("白城旅游数据导入完成！")

    def import_yushu_data(self):
        """导入榆树树旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (ys:City {name: '榆树', level: '县级市', description: '吉林省县级市，长春代管，中国北方粮仓，粮食产量大县'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (huayuanshan_fengjingqu:Attraction {name: '花园山旅游风景区', type: '自然景观', rating: 4.3, opening_hours: '8:00-17:00'}),
               (wukeshu_shidongyuan:Attraction {name: '五棵树湿地公园', type: '自然景观', rating: 4.2, opening_hours: '全天开放'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (yushu_dami:Food {name: '榆树大米', type: '地方特产', price_range: '低', description: '米粒饱满，口感香糯'}),
               (gandoufu:Food {name: '干豆腐', type: '地方特色', price_range: '低', description: '薄而韧，豆香浓郁'}),
               (yushu_binguan:Accommodation {name: '榆树宾馆', type: '三星级', price_range: '中低', rating: 4.2}),
               (yushu_dasha:Accommodation {name: '榆树大厦', type: '商务酒店', price_range: '中低', rating: 4.1}),
               (yushu_bus:Transportation {name: '榆树公交', type: '公交', route: '覆盖市区', price: '1-2元'}),
               (yushu_railway:Transportation {name: '榆树站', type: '火车', route: '通往长春等地', price: '根据里程'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '榆树'})
               WHERE a.name IN ['花园山旅游风景区', '五棵树湿地公园']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '榆树'}), (f:Food)
               WHERE f.name IN ['榆树大米', '干豆腐']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '五棵树湿地公园'}), (f:Food {name: '榆树大米'})
               CREATE (a)-[:NEAR_FOOD {distance: '1km', tip: '湿地公园周边农家可购新碾大米及米制品'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '五棵树湿地公园'}), (f:Food {name: '干豆腐'})
               CREATE (a)-[:NEAR_FOOD {distance: '800m', tip: '湿地附近豆腐坊可现做现吃干豆腐卷大葱'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '花园山旅游风景区'}), (f:Food {name: '干豆腐'})
               CREATE (a)-[:NEAR_FOOD {distance: '2km', tip: '景区山脚下餐馆有用干豆腐制作的农家菜'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '五棵树湿地公园'}), (ac:Accommodation {name: '榆树宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '5km', tip: '湿地游览后可休整，提供大米主食套餐'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '花园山旅游风景区'}), (ac:Accommodation {name: '榆树大厦'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '8km', tip: '山地游览后可休整，提供干豆腐特色菜'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '榆树'}), (t:Transportation)
               WHERE t.name IN ['榆树公交', '榆树站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '榆树公交'}), (t2:Transportation {name: '榆树站'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '公交直达火车站，方便前往长春、哈尔滨等地'}]->(t2)
           """)

        print("榆树旅游数据导入完成！")

    def import_dehui_data(self):
        """导入德惠旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (dh:City {name: '德惠', level: '县级市', description: '吉林省县级市，长春代管，中国肉鸡之乡，农产品加工基地'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (yuejin_shuiku:Attraction {name: '跃进水库', type: '自然景观', rating: 4.2, opening_hours: '全天开放'}),
               (dehui_gongyuan:Attraction {name: '德惠公园', type: '人文景观', rating: 4.1, opening_hours: '全天开放'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (dehui_rouji:Food {name: '德惠肉鸡', type: '地方特产', price_range: '中低', description: '肉质鲜嫩，营养丰富'}),
               (dehui_xiaoding:Food {name: '德惠小町大米', type: '地方特产', price_range: '低', description: '米质优良，口感香甜'}),
               (dehui_binguan:Accommodation {name: '德惠宾馆', type: '三星级', price_range: '中低', rating: 4.2}),
               (dehui_dongfang:Accommodation {name: '德惠东方宾馆', type: '商务酒店', price_range: '中低', rating: 4.1}),
               (dehui_bus:Transportation {name: '德惠公交', type: '公交', route: '覆盖市区', price: '1-2元'}),
               (dehui_railway:Transportation {name: '德惠站', type: '火车', route: '通往长春等地', price: '根据里程'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '德惠'})
               WHERE a.name IN ['跃进水库', '德惠公园']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '德惠'}), (f:Food)
               WHERE f.name IN ['德惠肉鸡', '德惠小町大米']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '跃进水库'}), (f:Food {name: '德惠肉鸡'})
               CREATE (a)-[:NEAR_FOOD {distance: '2km', tip: '水库周边农家乐可品尝炖肉鸡配山野菜'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '跃进水库'}), (f:Food {name: '德惠小町大米'})
               CREATE (a)-[:NEAR_FOOD {distance: '3km', tip: '水库附近米店可购真空包装小町大米'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '德惠公园'}), (f:Food {name: '德惠肉鸡'})
               CREATE (a)-[:NEAR_FOOD {distance: '1km', tip: '公园北门餐馆有炸鸡、卤鸡等肉鸡制品'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '跃进水库'}), (ac:Accommodation {name: '德惠宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '7km', tip: '垂钓休闲后可休整，提供肉鸡特色餐'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '德惠公园'}), (ac:Accommodation {name: '德惠东方宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '1.5km', tip: '公园游览后可便捷休整，提供大米主食'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '德惠'}), (t:Transportation)
               WHERE t.name IN ['德惠公交', '德惠站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '德惠公交'}), (t2:Transportation {name: '德惠站'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '公交直达火车站，方便前往长春、吉林等地'}]->(t2)
           """)

        print("德惠旅游数据导入完成！")

    def import_gongzhuling_data(self):
        """导入公主岭旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (gzl:City {name: '公主岭', level: '县级市', description: '吉林省县级市，长春代管，中国玉米之乡，国家现代农业示范区'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (nongye_kejiyuan:Attraction {name: '公主岭国家农业科技园区', type: '农业观光', rating: 4.4, opening_hours: '8:30-16:30'}),
               (ershijiazi_dujiaqu:Attraction {name: '二十家子旅游度假区', type: '自然景观', rating: 4.3, opening_hours: '全天开放'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (yumi_yan:Food {name: '玉米宴', type: '地方特色', price_range: '中低', description: '以玉米为主料，做法多样'}),
               (gongzhuling_dami:Food {name: '公主岭大米', type: '地方特产', price_range: '低', description: '米质优良，口感香糯'}),
               (gongzhuling_binguan:Accommodation {name: '公主岭宾馆', type: '三星级', price_range: '中低', rating: 4.3}),
               (gongzhuling_xiangling:Accommodation {name: '公主岭响铃宾馆', type: '商务酒店', price_range: '中低', rating: 4.2}),
               (gongzhuling_bus:Transportation {name: '公主岭公交', type: '公交', route: '覆盖市区', price: '1-2元'}),
               (gongzhuling_railway:Transportation {name: '公主岭站', type: '火车', route: '通往长春等地', price: '根据里程'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '公主岭'})
               WHERE a.name IN ['公主岭国家农业科技园区', '二十家子旅游度假区']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '公主岭'}), (f:Food)
               WHERE f.name IN ['玉米宴', '公主岭大米']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '公主岭国家农业科技园区'}), (f:Food {name: '玉米宴'})
               CREATE (a)-[:NEAR_FOOD {distance: '500m', tip: '园区内体验馆可品尝玉米馒头、玉米烙等特色菜品'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '公主岭国家农业科技园区'}), (f:Food {name: '公主岭大米'})
               CREATE (a)-[:NEAR_FOOD {distance: '800m', tip: '园区展销中心可购真空包装大米及米制品'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '二十家子旅游度假区'}), (f:Food {name: '玉米宴'})
               CREATE (a)-[:NEAR_FOOD {distance: '1.2km', tip: '度假区农家乐有用新鲜玉米制作的乡村宴席'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '公主岭国家农业科技园区'}), (ac:Accommodation {name: '公主岭宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '3km', tip: '农业观光后可休整，提供玉米宴特色餐'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '二十家子旅游度假区'}), (ac:Accommodation {name: '公主岭响铃宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '6km', tip: '度假区游览后可休整，提供大米主食套餐'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '公主岭'}), (t:Transportation)
               WHERE t.name IN ['公主岭公交', '公主岭站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '公主岭公交'}), (t2:Transportation {name: '公主岭站'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '公交直达火车站，方便前往长春、四平等地'}]->(t2)
           """)

        print("公主岭旅游数据导入完成！")

    def import_jiaohe_data(self):
        """导入蛟河旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (jh:City {name: '蛟河', level: '县级市', description: '吉林省县级市，吉林代管，中国黑木耳之乡，长白山下明珠'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (lafashan_gongyuan:Attraction {name: '拉法山国家森林公园', type: '自然景观', rating: 4.6, opening_hours: '8:00-17:00'}),
               (hongyegu:Attraction {name: '红叶谷', type: '自然景观', rating: 4.5, opening_hours: '全天开放'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (jiaohe_heimuer:Food {name: '蛟河黑木耳', type: '地方特产', price_range: '中低', description: '肉质厚实，营养丰富'}),
               (songhuahu_yuyan:Food {name: '松花湖鱼宴', type: '地方特色', price_range: '中', description: '野生湖鱼，鲜美异常'}),
               (jiaohe_binguan:Accommodation {name: '蛟河宾馆', type: '三星级', price_range: '中低', rating: 4.3}),
               (jiaohe_lafashan:Accommodation {name: '蛟河拉法山宾馆', type: '商务酒店', price_range: '中低', rating: 4.2}),
               (jiaohe_bus:Transportation {name: '蛟河公交', type: '公交', route: '覆盖市区', price: '1-2元'}),
               (jiaohe_railway:Transportation {name: '蛟河站', type: '火车', route: '通往吉林等地', price: '根据里程'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '蛟河'})
               WHERE a.name IN ['拉法山国家森林公园', '红叶谷']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '蛟河'}), (f:Food)
               WHERE f.name IN ['蛟河黑木耳', '松花湖鱼宴']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '红叶谷'}), (f:Food {name: '蛟河黑木耳'})
               CREATE (a)-[:NEAR_FOOD {distance: '1.5km', tip: '红叶谷景区商店可购干货，餐馆有木耳炒山鸡'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '红叶谷'}), (f:Food {name: '松花湖鱼宴'})
               CREATE (a)-[:NEAR_FOOD {distance: '4km', tip: '谷口松花湖支流畔餐馆可享现捕湖鱼宴'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '拉法山国家森林公园'}), (f:Food {name: '蛟河黑木耳'})
               CREATE (a)-[:NEAR_FOOD {distance: '2km', tip: '山脚下农家菜馆有用山泉水泡发的黑木耳菜品'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '红叶谷'}), (ac:Accommodation {name: '蛟河宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '8km', tip: '红叶观赏后可休整，提供黑木耳特色菜'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '拉法山国家森林公园'}), (ac:Accommodation {name: '蛟河拉法山宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '3km', tip: '山地游览后可休整，提供鱼宴晚餐'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '蛟河'}), (t:Transportation)
               WHERE t.name IN ['蛟河公交', '蛟河站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '蛟河公交'}), (t2:Transportation {name: '蛟河站'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '公交直达火车站，方便前往吉林、长春等地'}]->(t2)
           """)

        print("蛟河旅游数据导入完成！")

    def import_huadian_data(self):
        """导入桦甸旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (hd:City {name: '桦甸', level: '县级市', description: '吉林省县级市，吉林代管，中国黄金之乡，林海雪原之城'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (hongshi_gongyuan:Attraction {name: '红石国家森林公园', type: '自然景观', rating: 4.5, opening_hours: '8:00-17:00'}),
               (baishanhhu:Attraction {name: '白山湖', type: '自然景观', rating: 4.4, opening_hours: '全天开放'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (huadian_linwa:Food {name: '桦甸林蛙', type: '地方特产', price_range: '中高', description: '滋补珍品，肉质细嫩'}),
               (songzi:Food {name: '松子', type: '地方特产', price_range: '中低', description: '粒大饱满，香味浓郁'}),
               (huadian_binguan:Accommodation {name: '桦甸宾馆', type: '三星级', price_range: '中低', rating: 4.3}),
               (huadian_jincheng:Accommodation {name: '桦甸金城宾馆', type: '商务酒店', price_range: '中低', rating: 4.2}),
               (huadian_bus:Transportation {name: '桦甸公交', type: '公交', route: '覆盖市区', price: '1-2元'}),
               (huadian_railway:Transportation {name: '桦甸站', type: '火车', route: '通往吉林等地', price: '根据里程'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '桦甸'})
               WHERE a.name IN ['红石国家森林公园', '白山湖']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '桦甸'}), (f:Food)
               WHERE f.name IN ['桦甸林蛙', '松子']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '红石国家森林公园'}), (f:Food {name: '桦甸林蛙'})
               CREATE (a)-[:NEAR_FOOD {distance: '2km', tip: '森林公园内度假村可品尝林蛙炖土豆等特色菜'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '红石国家森林公园'}), (f:Food {name: '松子'})
               CREATE (a)-[:NEAR_FOOD {distance: '1km', tip: '景区商店有售原味松子及松子制品'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '白山湖'}), (f:Food {name: '松子'})
               CREATE (a)-[:NEAR_FOOD {distance: '3km', tip: '湖边特产店可购新鲜采摘的松子'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '红石国家森林公园'}), (ac:Accommodation {name: '桦甸宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '15km', tip: '森林游览后可休整，提供林蛙滋补餐'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '白山湖'}), (ac:Accommodation {name: '桦甸金城宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '20km', tip: '湖景游览后可休整，提供松子特色点心'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '桦甸'}), (t:Transportation)
               WHERE t.name IN ['桦甸公交', '桦甸站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '桦甸公交'}), (t2:Transportation {name: '桦甸站'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '公交直达火车站，方便前往吉林、长春等地'}]->(t2)
           """)

        print("桦甸旅游数据导入完成！")

    def import_shulan_data(self):
        """导入舒兰旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (sl:City {name: '舒兰', level: '县级市', description: '吉林省县级市，吉林代管，中国生态稻米之乡，贡米产地'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (fenghuangshan:Attraction {name: '凤凰山', type: '自然景观', rating: 4.3, opening_hours: '8:00-17:00'}),
               (liangjiashan_shuiku:Attraction {name: '亮甲山水库', type: '自然景观', rating: 4.2, opening_hours: '全天开放'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (shulan_dami:Food {name: '舒兰大米', type: '地方特产', price_range: '中低', description: '米质优良，历史上为贡米'}),
               (niandoubao:Food {name: '粘豆包', type: '传统小吃', price_range: '低', description: '软糯香甜，东北特色'}),
               (shulan_binguan:Accommodation {name: '舒兰宾馆', type: '三星级', price_range: '中低', rating: 4.2}),
               (shulan_jinzhou:Accommodation {name: '舒兰金洲酒店', type: '商务酒店', price_range: '中低', rating: 4.1}),
               (shulan_bus:Transportation {name: '舒兰公交', type: '公交', route: '覆盖市区', price: '1-2元'}),
               (shulan_railway:Transportation {name: '舒兰站', type: '火车', route: '通往吉林等地', price: '根据里程'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '舒兰'})
               WHERE a.name IN ['凤凰山', '亮甲山水库']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '舒兰'}), (f:Food)
               WHERE f.name IN ['舒兰大米', '粘豆包']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '亮甲山水库'}), (f:Food {name: '舒兰大米'})
               CREATE (a)-[:NEAR_FOOD {distance: '1.5km', tip: '水库周边米厂可购新米，餐馆有用贡米制作的米饭'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '亮甲山水库'}), (f:Food {name: '粘豆包'})
               CREATE (a)-[:NEAR_FOOD {distance: '1km', tip: '水库边农家可品尝现蒸粘豆包配白糖'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '凤凰山'}), (f:Food {name: '粘豆包'})
               CREATE (a)-[:NEAR_FOOD {distance: '2km', tip: '山脚下农家乐有传统工艺制作的粘豆包'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '亮甲山水库'}), (ac:Accommodation {name: '舒兰宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '8km', tip: '湖景游览后可休整，提供大米主食套餐'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '凤凰山'}), (ac:Accommodation {name: '舒兰金洲酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '10km', tip: '山地游览后可休整，提供粘豆包早餐'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '舒兰'}), (t:Transportation)
               WHERE t.name IN ['舒兰公交', '舒兰站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '舒兰公交'}), (t2:Transportation {name: '舒兰站'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '公交直达火车站，方便前往吉林、哈尔滨等地'}]->(t2)
           """)

        print("舒兰旅游数据导入完成！")

    def import_panshi_data(self):
        """导入磐石旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (ps:City {name: '磐石', level: '县级市', description: '吉林省县级市，吉林代管，中国镍业之乡，抗日根据地'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (huanghe_shuiku:Attraction {name: '黄河水库', type: '自然景观', rating: 4.4, opening_hours: '全天开放'}),
               (guanma_rongdong:Attraction {name: '官马溶洞', type: '自然景观', rating: 4.5, opening_hours: '8:30-17:00'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (panshi_shiyongjun:Food {name: '磐石食用菌', type: '地方特产', price_range: '中低', description: '品种丰富，营养健康'}),
               (shanyecai:Food {name: '山野菜', type: '地方特色', price_range: '低', description: '天然无污染，时令鲜美'}),
               (panshi_binguan:Accommodation {name: '磐石宾馆', type: '三星级', price_range: '中低', rating: 4.3}),
               (panshi_niedu:Accommodation {name: '磐石镍都宾馆', type: '商务酒店', price_range: '中低', rating: 4.2}),
               (panshi_bus:Transportation {name: '磐石公交', type: '公交', route: '覆盖市区', price: '1-2元'}),
               (panshi_railway:Transportation {name: '磐石站', type: '火车', route: '通往吉林等地', price: '根据里程'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '磐石'})
               WHERE a.name IN ['黄河水库', '官马溶洞']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '磐石'}), (f:Food)
               WHERE f.name IN ['磐石食用菌', '山野菜']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '官马溶洞'}), (f:Food {name: '磐石食用菌'})
               CREATE (a)-[:NEAR_FOOD {distance: '1km', tip: '溶洞出口餐馆有用本地菌类制作的火锅'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '官马溶洞'}), (f:Food {name: '山野菜'})
               CREATE (a)-[:NEAR_FOOD {distance: '800m', tip: '溶洞周边农家可品尝现采山野菜蘸酱'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '黄河水库'}), (f:Food {name: '山野菜'})
               CREATE (a)-[:NEAR_FOOD {distance: '1.5km', tip: '水库畔农家乐有多种凉拌山野菜'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '官马溶洞'}), (ac:Accommodation {name: '磐石宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '5km', tip: '溶洞探秘后可休整，提供食用菌特色餐'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '黄河水库'}), (ac:Accommodation {name: '磐石镍都宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '8km', tip: '水库游览后可休整，提供山野菜拼盘'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '磐石'}), (t:Transportation)
               WHERE t.name IN ['磐石公交', '磐石站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '磐石公交'}), (t2:Transportation {name: '磐石站'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '公交直达火车站，方便前往吉林、长春等地'}]->(t2)
           """)

        print("磐石旅游数据导入完成！")

    def import_shuangliao_data(self):
        """导入双辽旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (sl:City {name: '双辽', level: '县级市', description: '吉林省县级市，四平代管，吉林西部重要节点，农牧业基地'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (yimashu_gongyuan:Attraction {name: '一马树森林公园', type: '自然景观', rating: 4.3, opening_hours: '8:00-17:00'}),
               (zhengjiatun_bowuguan:Attraction {name: '郑家屯博物馆', type: '人文景观', rating: 4.2, opening_hours: '9:00-16:30'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (shuangliao_huasheng:Food {name: '双辽花生', type: '地方特产', price_range: '低', description: '粒大饱满，香脆可口'}),
               (caoyuan_rou:Food {name: '草原牛羊肉', type: '地方特色', price_range: '中', description: '肉质鲜美，草原风味'}),
               (shuangliao_binguan:Accommodation {name: '双辽宾馆', type: '三星级', price_range: '中低', rating: 4.2}),
               (shuangliao_dianli:Accommodation {name: '双辽电力宾馆', type: '商务酒店', price_range: '中低', rating: 4.1}),
               (shuangliao_bus:Transportation {name: '双辽公交', type: '公交', route: '覆盖市区', price: '1-2元'}),
               (shuangliao_railway:Transportation {name: '双辽站', type: '火车', route: '通往四平等地', price: '根据里程'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '双辽'})
               WHERE a.name IN ['一马树森林公园', '郑家屯博物馆']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '双辽'}), (f:Food)
               WHERE f.name IN ['双辽花生', '草原牛羊肉']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '一马树森林公园'}), (f:Food {name: '双辽花生'})
               CREATE (a)-[:NEAR_FOOD {distance: '1km', tip: '森林公园特产店有售原味及五香花生'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '一马树森林公园'}), (f:Food {name: '草原牛羊肉'})
               CREATE (a)-[:NEAR_FOOD {distance: '2km', tip: '公园外蒙古包餐厅可享手抓牛羊肉'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '郑家屯博物馆'}), (f:Food {name: '双辽花生'})
               CREATE (a)-[:NEAR_FOOD {distance: '800m', tip: '博物馆周边商店有售花生糖等制品'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '一马树森林公园'}), (ac:Accommodation {name: '双辽宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '6km', tip: '森林浴后可休整，提供草原牛羊肉餐'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '郑家屯博物馆'}), (ac:Accommodation {name: '双辽电力宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '1.2km', tip: '文化参观后可休整，提供花生特色小吃'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '双辽'}), (t:Transportation)
               WHERE t.name IN ['双辽公交', '双辽站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '双辽公交'}), (t2:Transportation {name: '双辽站'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '公交直达火车站，方便前往四平、通辽等地'}]->(t2)
           """)

        print("双辽旅游数据导入完成！")

    def import_meihekou_data(self):
        """导入梅河口旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (mhk:City {name: '梅河口', level: '县级市', description: '吉林省县级市，省直管，中国皇粮贡米之乡，东北商贸重镇'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (jiguanshan_gongyuan:Attraction {name: '鸡冠山国家森林公园', type: '自然景观', rating: 4.6, opening_hours: '8:00-17:00'}),
               (hailonghu_jingqu:Attraction {name: '海龙湖景区', type: '自然景观', rating: 4.5, opening_hours: '全天开放'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (meihe_dami:Food {name: '梅河大米', type: '地方特产', price_range: '中低', description: '米中精品，历史上为贡米'}),
               (meihekou_laomian:Food {name: '梅河口冷面', type: '地方小吃', price_range: '低', description: '面条筋道，汤底鲜美'}),
               (meihekou_jianguo:Accommodation {name: '梅河口建国饭店', type: '四星级', price_range: '中', rating: 4.5}),
               (meihekou_jinding:Accommodation {name: '梅河口金鼎大酒店', type: '商务酒店', price_range: '中低', rating: 4.3}),
               (meihekou_bus:Transportation {name: '梅河口公交', type: '公交', route: '覆盖市区', price: '1-2元'}),
               (meihekou_railway:Transportation {name: '梅河口站', type: '火车', route: '通往沈阳、长春等地', price: '根据里程'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '梅河口'})
               WHERE a.name IN ['鸡冠山国家森林公园', '海龙湖景区']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '梅河口'}), (f:Food)
               WHERE f.name IN ['梅河大米', '梅河口冷面']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '海龙湖景区'}), (f:Food {name: '梅河大米'})
               CREATE (a)-[:NEAR_FOOD {distance: '1km', tip: '景区周边米店可购贡米，餐馆有用新米制作的米饭'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '海龙湖景区'}), (f:Food {name: '梅河口冷面'})
               CREATE (a)-[:NEAR_FOOD {distance: '800m', tip: '湖岸小吃街有现压冷面配本地辣白菜'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '鸡冠山国家森林公园'}), (f:Food {name: '梅河口冷面'})
               CREATE (a)-[:NEAR_FOOD {distance: '2km', tip: '山脚下餐馆有冰镇冷面，适合登山后食用'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '海龙湖景区'}), (ac:Accommodation {name: '梅河口建国饭店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '3km', tip: '湖景观光后可休整，提供大米主食套餐'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '鸡冠山国家森林公园'}), (ac:Accommodation {name: '梅河口金鼎大酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '10km', tip: '山地游览后可休整，提供冷面特色餐'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '梅河口'}), (t:Transportation)
               WHERE t.name IN ['梅河口公交', '梅河口站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '梅河口公交'}), (t2:Transportation {name: '梅河口站'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '公交直达火车站，方便前往沈阳、长春等地'}]->(t2)
           """)

        print("梅河口旅游数据导入完成！")

    def import_jian_data(self):
        """导入集安旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (ja:City {name: '集安', level: '县级市', description: '吉林省县级市，通化代管，世界文化遗产地，高句丽古都'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (gaogouli_wangcheng:Attraction {name: '高句丽王城', type: '人文景观', rating: 4.8, opening_hours: '8:30-17:00'}),
               (wunvfeng_gongyuan:Attraction {name: '五女峰国家森林公园', type: '自然景观', rating: 4.7, opening_hours: '8:00-17:00'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (jian_biantiaoshen:Food {name: '集安边条参', type: '地方特产', price_range: '中高', description: '滋补珍品，药食同源'}),
               (yalujiang_yuyan:Food {name: '鸭绿江鱼宴', type: '地方特色', price_range: '中', description: '江鱼鲜美，做法多样'}),
               (jian_xiangzhou:Accommodation {name: '集安香洲花园酒店', type: '四星级', price_range: '中', rating: 4.6}),
               (jian_binguan:Accommodation {name: '集安宾馆', type: '商务酒店', price_range: '中低', rating: 4.4}),
               (jian_bus:Transportation {name: '集安公交', type: '公交', route: '覆盖市区', price: '1-2元'}),
               (jian_railway:Transportation {name: '集安站', type: '火车', route: '通往通化等地', price: '根据里程'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '集安'})
               WHERE a.name IN ['高句丽王城', '五女峰国家森林公园']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '集安'}), (f:Food)
               WHERE f.name IN ['集安边条参', '鸭绿江鱼宴']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '高句丽王城'}), (f:Food {name: '集安边条参'})
               CREATE (a)-[:NEAR_FOOD {distance: '1.5km', tip: '王城景区商店有售参茶及参制品礼盒'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '高句丽王城'}), (f:Food {name: '鸭绿江鱼宴'})
               CREATE (a)-[:NEAR_FOOD {distance: '2km', tip: '王城附近江鲜馆有用鸭绿江鱼制作的宴席'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '五女峰国家森林公园'}), (f:Food {name: '鸭绿江鱼宴'})
               CREATE (a)-[:NEAR_FOOD {distance: '5km', tip: '森林公园出口处江畔餐馆可享现捕江鱼'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '高句丽王城'}), (ac:Accommodation {name: '集安香洲花园酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '3km', tip: '文化遗产探访后可休整，提供鱼宴特色餐'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '五女峰国家森林公园'}), (ac:Accommodation {name: '集安宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '8km', tip: '山地游览后可休整，提供参汤滋补品'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '集安'}), (t:Transportation)
               WHERE t.name IN ['集安公交', '集安站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '集安公交'}), (t2:Transportation {name: '集安站'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '公交直达火车站，方便前往通化、丹东等地'}]->(t2)
           """)

        print("集安旅游数据导入完成！")

    def import_linjiang_data(self):
        """导入临江旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (lj:City {name: '临江', level: '县级市', description: '吉林省县级市，白山代管，中朝边境口岸，红色旅游胜地'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (sibao_jinianguan:Attraction {name: '四保临江战役纪念馆', type: '人文景观', rating: 4.6, opening_hours: '9:00-16:30'}),
               (chenyun_jiuju:Attraction {name: '陈云旧居', type: '人文景观', rating: 4.5, opening_hours: '9:00-16:00'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (linjiang_gourou:Food {name: '临江狗肉', type: '地方特色', price_range: '中', description: '肉质鲜美，温补养生'}),
               (yalujiang_liyu:Food {name: '鸭绿江鲤鱼', type: '地方特色', price_range: '中', description: '江鱼肥美，做法多样'}),
               (linjiang_binguan:Accommodation {name: '临江宾馆', type: '三星级', price_range: '中低', rating: 4.3}),
               (linjiang_bianjing:Accommodation {name: '临江边境大酒店', type: '商务酒店', price_range: '中低', rating: 4.2}),
               (linjiang_bus:Transportation {name: '临江公交', type: '公交', route: '覆盖市区', price: '1-2元'}),
               (linjiang_railway:Transportation {name: '临江站', type: '火车', route: '通往白山等地', price: '根据里程'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '临江'})
               WHERE a.name IN ['四保临江战役纪念馆', '陈云旧居']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '临江'}), (f:Food)
               WHERE f.name IN ['临江狗肉', '鸭绿江鲤鱼']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '四保临江战役纪念馆'}), (f:Food {name: '临江狗肉'})
               CREATE (a)-[:NEAR_FOOD {distance: '1km', tip: '纪念馆附近餐馆有狗肉火锅、酱狗肉等特色做法'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '四保临江战役纪念馆'}), (f:Food {name: '鸭绿江鲤鱼'})
               CREATE (a)-[:NEAR_FOOD {distance: '1.5km', tip: '纪念馆周边江鲜馆可品尝红烧鲤鱼、清蒸鲤鱼'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '陈云旧居'}), (f:Food {name: '鸭绿江鲤鱼'})
               CREATE (a)-[:NEAR_FOOD {distance: '800m', tip: '旧居附近餐馆有用鸭绿江活水养殖的鲤鱼菜品'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '四保临江战役纪念馆'}), (ac:Accommodation {name: '临江宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '2km', tip: '红色历史学习后可休整，提供狗肉特色餐'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '陈云旧居'}), (ac:Accommodation {name: '临江边境大酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '1.2km', tip: '革命旧址参观后可休整，提供江鱼晚餐'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '临江'}), (t:Transportation)
               WHERE t.name IN ['临江公交', '临江站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '临江公交'}), (t2:Transportation {name: '临江站'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '公交直达火车站，方便前往白山、通化等地'}]->(t2)
           """)

        print("临江旅游数据导入完成！")

    def import_fuyu_data(self):
        """导入扶余旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (fy:City {name: '扶余', level: '县级市', description: '吉林省县级市，松原代管，古夫余国故地，辽金文化名城'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (dajin_beibei:Attraction {name: '大金得胜陀颂碑', type: '人文景观', rating: 4.4, opening_hours: '9:00-16:30'}),
               (fuyu_gongyuan:Attraction {name: '扶余公园', type: '人文景观', rating: 4.3, opening_hours: '全天开放'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (fuyu_huasheng:Food {name: '扶余花生', type: '地方特产', price_range: '低', description: '粒大饱满，香脆可口'}),
               (sanqingshan_fentiao:Food {name: '三青山粉条', type: '地方特产', price_range: '低', description: '口感爽滑，久煮不烂'}),
               (fuyu_binguan:Accommodation {name: '扶余宾馆', type: '三星级', price_range: '中低', rating: 4.2}),
               (fuyu_liangmao:Accommodation {name: '扶余粮贸大厦', type: '商务酒店', price_range: '中低', rating: 4.1}),
               (fuyu_bus:Transportation {name: '扶余公交', type: '公交', route: '覆盖市区', price: '1-2元'}),
               (fuyu_railway:Transportation {name: '扶余站', type: '火车', route: '通往松原等地', price: '根据里程'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '扶余'})
               WHERE a.name IN ['大金得胜陀颂碑', '扶余公园']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '扶余'}), (f:Food)
               WHERE f.name IN ['扶余花生', '三青山粉条']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '扶余公园'}), (f:Food {name: '扶余花生'})
               CREATE (a)-[:NEAR_FOOD {distance: '500m', tip: '公园门口市场有售炒花生、花生酥等制品'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '扶余公园'}), (f:Food {name: '三青山粉条'})
               CREATE (a)-[:NEAR_FOOD {distance: '800m', tip: '公园周边特产店可购纯土豆粉条'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '大金得胜陀颂碑'}), (f:Food {name: '三青山粉条'})
               CREATE (a)-[:NEAR_FOOD {distance: '2km', tip: '碑刻景区商店有售粉条礼盒，适合馈赠'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '扶余公园'}), (ac:Accommodation {name: '扶余宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '1.5km', tip: '公园游览后可休整，提供花生特色小吃'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '大金得胜陀颂碑'}), (ac:Accommodation {name: '扶余粮贸大厦'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '3km', tip: '辽金文化探访后可休整，提供粉条炖菜'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '扶余'}), (t:Transportation)
               WHERE t.name IN ['扶余公交', '扶余站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '扶余公交'}), (t2:Transportation {name: '扶余站'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '公交直达火车站，方便前往松原、长春等地'}]->(t2)
           """)

        print("扶余旅游数据导入完成！")

    def import_taonan_data(self):
        """导入洮南旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (tn:City {name: '洮南', level: '县级市', description: '吉林省县级市，白城代管，千年府邸，百年古镇'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (aoniushan_fengjingqu:Attraction {name: '敖牛山风景区', type: '自然景观', rating: 4.4, opening_hours: '8:00-17:00'}),
               (wujunsheng_jiuzhi:Attraction {name: '吴俊升商业大楼旧址', type: '人文景观', rating: 4.3, opening_hours: '9:00-16:30'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (taonan_xiangjiu:Food {name: '洮南香酒', type: '地方特产', price_range: '中低', description: '酒香浓郁，口感醇厚'}),
               (heishui_xigua:Food {name: '黑水西瓜', type: '地方特产', price_range: '低', description: '皮薄多汁，甘甜爽口'}),
               (taonan_binguan:Accommodation {name: '洮南宾馆', type: '三星级', price_range: '中低', rating: 4.3}),
               (taonan_wanhou:Accommodation {name: '洮南万豪酒店', type: '商务酒店', price_range: '中低', rating: 4.2}),
               (taonan_bus:Transportation {name: '洮南公交', type: '公交', route: '覆盖市区', price: '1-2元'}),
               (taonan_railway:Transportation {name: '洮南站', type: '火车', route: '通往白城等地', price: '根据里程'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '洮南'})
               WHERE a.name IN ['敖牛山风景区', '吴俊升商业大楼旧址']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '洮南'}), (f:Food)
               WHERE f.name IN ['洮南香酒', '黑水西瓜']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '敖牛山风景区'}), (f:Food {name: '洮南香酒'})
               CREATE (a)-[:NEAR_FOOD {distance: '3km', tip: '景区山脚下酒馆可品尝原浆香酒配农家菜'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '敖牛山风景区'}), (f:Food {name: '黑水西瓜'})
               CREATE (a)-[:NEAR_FOOD {distance: '2km', tip: '景区出口处瓜农直销新鲜黑水西瓜'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '吴俊升商业大楼旧址'}), (f:Food {name: '洮南香酒'})
               CREATE (a)-[:NEAR_FOOD {distance: '500m', tip: '旧址周边酒坊有售百年工艺酿造的香酒'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '敖牛山风景区'}), (ac:Accommodation {name: '洮南宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '10km', tip: '山地观光后可休整，提供西瓜甜品'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '吴俊升商业大楼旧址'}), (ac:Accommodation {name: '洮南万豪酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '800m', tip: '古镇探访后可休整，提供香酒品鉴'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '洮南'}), (t:Transportation)
               WHERE t.name IN ['洮南公交', '洮南站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '洮南公交'}), (t2:Transportation {name: '洮南站'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '公交直达火车站，方便前往白城、松原等地'}]->(t2)
           """)

        print("洮南旅游数据导入完成！")

    def import_da_an_data(self):
        """导入大安旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (da:City {name: '大安', level: '县级市', description: '吉林省县级市，白城代管，鱼米之乡，嫩江明珠'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (nenjiangwan_shidi:Attraction {name: '嫩江湾国家湿地公园', type: '自然景观', rating: 4.6, opening_hours: '8:00-17:30'}),
               (wujianfang_leyuan:Attraction {name: '五间房水岛乐园', type: '自然景观', rating: 4.4, opening_hours: '9:00-17:00'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (daan_kaoge:Food {name: '大安烤鸽', type: '地方特色', price_range: '中', description: '外焦里嫩，香味浓郁'}),
               (nenjiang_yuyan:Food {name: '嫩江鱼宴', type: '地方特色', price_range: '中', description: '江鱼鲜美，做法多样'}),
               (daan_binguan:Accommodation {name: '大安宾馆', type: '三星级', price_range: '中低', rating: 4.3}),
               (daan_nenjiangwan:Accommodation {name: '大安嫩江湾酒店', type: '商务酒店', price_range: '中低', rating: 4.2}),
               (daan_bus:Transportation {name: '大安公交', type: '公交', route: '覆盖市区', price: '1-2元'}),
               (daan_railway:Transportation {name: '大安站', type: '火车', route: '通往白城等地', price: '根据里程'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '大安'})
               WHERE a.name IN ['嫩江湾国家湿地公园', '五间房水岛乐园']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '大安'}), (f:Food)
               WHERE f.name IN ['大安烤鸽', '嫩江鱼宴']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '嫩江湾国家湿地公园'}), (f:Food {name: '嫩江鱼宴'})
               CREATE (a)-[:NEAR_FOOD {distance: '1km', tip: '湿地公园畔渔家乐可享现捕现做的江鱼宴'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '嫩江湾国家湿地公园'}), (f:Food {name: '大安烤鸽'})
               CREATE (a)-[:NEAR_FOOD {distance: '1.5km', tip: '湿地出口处烧烤街有特色烤鸽配啤酒'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '五间房水岛乐园'}), (f:Food {name: '嫩江鱼宴'})
               CREATE (a)-[:NEAR_FOOD {distance: '2km', tip: '水岛周边餐馆有用活水养殖的江鱼菜品'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '嫩江湾国家湿地公园'}), (ac:Accommodation {name: '大安宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '3km', tip: '湿地生态游览后可休整，提供鱼宴晚餐'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '五间房水岛乐园'}), (ac:Accommodation {name: '大安嫩江湾酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '5km', tip: '水岛游玩后可休整，提供烤鸽特色餐'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '大安'}), (t:Transportation)
               WHERE t.name IN ['大安公交', '大安站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '大安公交'}), (t2:Transportation {name: '大安站'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '公交直达火车站，方便前往白城、齐齐哈尔等地'}]->(t2)
           """)

        print("大安旅游数据导入完成！")

    def import_yanji_data(self):
        """导入延吉旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (yj:City {name: '延吉', level: '县级市', description: '吉林省县级市，延边州首府，中国朝鲜族文化中心'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (maoershan_gongyuan:Attraction {name: '帽儿山国家森林公园', type: '自然景观', rating: 4.7, opening_hours: '8:00-17:00'}),
               (chaoxianzu_minzuyuan:Attraction {name: '中国朝鲜族民俗园', type: '人文景观', rating: 4.6, opening_hours: '9:00-17:00'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (yanji_laomian:Food {name: '延吉冷面', type: '地方特色', price_range: '中低', description: '面条筋道，汤底冰爽'}),
               (shiguo_banfan:Food {name: '石锅拌饭', type: '朝鲜族美食', price_range: '中低', description: '配料丰富，锅巴香脆'}),
               (yanji_kailuosi:Accommodation {name: '延吉卡伊洛斯酒店', type: '五星级', price_range: '高', rating: 4.7}),
               (yanji_binguan:Accommodation {name: '延吉宾馆', type: '四星级', price_range: '中', rating: 4.5}),
               (yanji_bus:Transportation {name: '延吉公交', type: '公交', route: '覆盖市区', price: '1-2元'}),
               (yanji_xizhan:Transportation {name: '延吉西站', type: '高铁', route: '通往长春等地', price: '根据里程'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '延吉'})
               WHERE a.name IN ['帽儿山国家森林公园', '中国朝鲜族民俗园']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '延吉'}), (f:Food)
               WHERE f.name IN ['延吉冷面', '石锅拌饭']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '中国朝鲜族民俗园'}), (f:Food {name: '延吉冷面'})
               CREATE (a)-[:NEAR_FOOD {distance: '500m', tip: '民俗园内朝鲜族餐馆有现压荞麦冷面'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '中国朝鲜族民俗园'}), (f:Food {name: '石锅拌饭'})
               CREATE (a)-[:NEAR_FOOD {distance: '300m', tip: '民俗园美食街有传统铜锅拌饭'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '帽儿山国家森林公园'}), (f:Food {name: '延吉冷面'})
               CREATE (a)-[:NEAR_FOOD {distance: '2km', tip: '山脚下韩式餐馆有冰镇冷面，适合登山后食用'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '中国朝鲜族民俗园'}), (ac:Accommodation {name: '延吉卡伊洛斯酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '3km', tip: '文化体验后可休整，提供韩式自助晚餐'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '帽儿山国家森林公园'}), (ac:Accommodation {name: '延吉宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '4km', tip: '山地游览后可休整，提供石锅拌饭早餐'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '延吉'}), (t:Transportation)
               WHERE t.name IN ['延吉公交', '延吉西站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '延吉公交'}), (t2:Transportation {name: '延吉西站'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '公交专线直达高铁站，方便前往长春、沈阳等地'}]->(t2)
           """)

        print("延吉旅游数据导入完成！")

    def import_tumen_data(self):
        """导入图们旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (tm:City {name: '图们', level: '县级市', description: '吉林省县级市，延边州代管，中朝边境口岸，图们江畔明珠'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (tumenjiang_gongyuan:Attraction {name: '图们江公园', type: '自然景观', rating: 4.5, opening_hours: '全天开放'}),
               (tumen_kouan:Attraction {name: '图们口岸', type: '人文景观', rating: 4.4, opening_hours: '9:00-16:30'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (jiangmi_ji:Food {name: '江米鸡', type: '地方特色', price_range: '中', description: '鸡肉鲜嫩，米饭香糯'}),
               (dagao:Food {name: '打糕', type: '朝鲜族美食', price_range: '低', description: '软糯香甜，传统风味'}),
               (tumenjiang_dajiudian:Accommodation {name: '图们江大酒店', type: '三星级', price_range: '中低', rating: 4.3}),
               (tumen_binguan:Accommodation {name: '图们宾馆', type: '商务酒店', price_range: '中低', rating: 4.2}),
               (tumen_bus:Transportation {name: '图们公交', type: '公交', route: '覆盖市区', price: '1-2元'}),
               (tumen_zhan:Transportation {name: '图们站', type: '火车', route: '通往延吉等地', price: '根据里程'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '图们'})
               WHERE a.name IN ['图们江公园', '图们口岸']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '图们'}), (f:Food)
               WHERE f.name IN ['江米鸡', '打糕']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '图们江公园'}), (f:Food {name: '江米鸡'})
               CREATE (a)-[:NEAR_FOOD {distance: '800m', tip: '江畔朝鲜族餐馆有传统铁锅江米鸡'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '图们江公园'}), (f:Food {name: '打糕'})
               CREATE (a)-[:NEAR_FOOD {distance: '500m', tip: '公园门口有现做打糕，可配黄豆粉食用'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '图们口岸'}), (f:Food {name: '打糕'})
               CREATE (a)-[:NEAR_FOOD {distance: '1km', tip: '口岸景区商店有售真空包装打糕'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '图们江公园'}), (ac:Accommodation {name: '图们江大酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '1.2km', tip: '边境风光游览后可休整，提供江米鸡特色餐'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '图们口岸'}), (ac:Accommodation {name: '图们宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '1.5km', tip: '口岸参观后可休整，提供打糕早餐'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '图们'}), (t:Transportation)
               WHERE t.name IN ['图们公交', '图们站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '图们公交'}), (t2:Transportation {name: '图们站'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '公交直达火车站，方便前往延吉、珲春等地'}]->(t2)
           """)

        print("图们旅游数据导入完成！")

    def import_dunhua_data(self):
        """导入敦化旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (dh:City {name: '敦化', level: '县级市', description: '吉林省县级市，延边州代管，千年古都百年县，敖东古城'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (liudingshan_qu:Attraction {name: '六鼎山文化旅游区', type: '人文景观', rating: 4.7, opening_hours: '8:00-17:00'}),
               (zhengjue_si:Attraction {name: '正觉寺', type: '人文景观', rating: 4.6, opening_hours: '8:30-16:30'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (dunhua_xiaodou:Food {name: '敦化小土豆', type: '地方特产', price_range: '低', description: '口感绵密，品质优良'}),
               (chaoxianzu_paocai:Food {name: '朝鲜族泡菜', type: '地方特色', price_range: '低', description: '酸辣爽口，开胃下饭'}),
               (dunhua_wanhou:Accommodation {name: '敦化万豪国际酒店', type: '四星级', price_range: '中', rating: 4.5}),
               (dunhua_binguan:Accommodation {name: '敦化宾馆', type: '商务酒店', price_range: '中低', rating: 4.3}),
               (dunhua_bus:Transportation {name: '敦化公交', type: '公交', route: '覆盖市区', price: '1-2元'}),
               (dunhua_zhan:Transportation {name: '敦化站', type: '火车', route: '通往长春等地', price: '根据里程'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '敦化'})
               WHERE a.name IN ['六鼎山文化旅游区', '正觉寺']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '敦化'}), (f:Food)
               WHERE f.name IN ['敦化小土豆', '朝鲜族泡菜']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '六鼎山文化旅游区'}), (f:Food {name: '敦化小土豆'})
               CREATE (a)-[:NEAR_FOOD {distance: '1km', tip: '景区配套餐厅有土豆炖豆角、炕烤小土豆等特色菜'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '六鼎山文化旅游区'}), (f:Food {name: '朝鲜族泡菜'})
               CREATE (a)-[:NEAR_FOOD {distance: '800m', tip: '景区美食街有辣白菜、萝卜泡菜等十几种朝鲜族泡菜'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '正觉寺'}), (f:Food {name: '朝鲜族泡菜'})
               CREATE (a)-[:NEAR_FOOD {distance: '500m', tip: '寺院周边素菜馆有用泡菜制作的斋菜'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '六鼎山文化旅游区'}), (ac:Accommodation {name: '敦化万豪国际酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '3km', tip: '文化游览后可休整，提供土豆宴特色餐'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '正觉寺'}), (ac:Accommodation {name: '敦化宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '2km', tip: '寺院参观后可休整，提供泡菜拼盘佐餐'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '敦化'}), (t:Transportation)
               WHERE t.name IN ['敦化公交', '敦化站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '敦化公交'}), (t2:Transportation {name: '敦化站'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '公交直达火车站，方便前往长春、延吉等地'}]->(t2)
           """)

        print("敦化旅游数据导入完成！")

    def import_hunchun_data(self):
        """导入珲春旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (hc:City {name: '珲春', level: '县级市', description: '吉林省县级市，延边州代管，中俄朝三国交界，东北亚金三角'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (fangchuan_fengjingqu:Attraction {name: '防川风景区', type: '自然景观', rating: 4.8, opening_hours: '8:00-17:00'}),
               (tuzipai:Attraction {name: '土字牌', type: '人文景观', rating: 4.5, opening_hours: '全天开放'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (hunchun_diwangxie:Food {name: '珲春帝王蟹', type: '地方特色', price_range: '高', description: '肉质鲜美，体型硕大'}),
               (eluosi_dalieba:Food {name: '俄罗斯大列巴', type: '异国风味', price_range: '中低', description: '外脆内软，麦香浓郁'}),
               (hunchun_minzu:Accommodation {name: '珲春民族花园国际酒店', type: '四星级', price_range: '中', rating: 4.6}),
               (hunchun_binguan:Accommodation {name: '珲春宾馆', type: '商务酒店', price_range: '中低', rating: 4.3}),
               (hunchun_bus:Transportation {name: '珲春公交', type: '公交', route: '覆盖市区', price: '1-2元'}),
               (hunchun_zhan:Transportation {name: '珲春站', type: '火车', route: '通往延吉等地', price: '根据里程'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '珲春'})
               WHERE a.name IN ['防川风景区', '土字牌']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '珲春'}), (f:Food)
               WHERE f.name IN ['珲春帝王蟹', '俄罗斯大列巴']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '防川风景区'}), (f:Food {name: '珲春帝王蟹'})
               CREATE (a)-[:NEAR_FOOD {distance: '2km', tip: '景区出口海鲜馆有现捕帝王蟹，可清蒸或芝士焗'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '防川风景区'}), (f:Food {name: '俄罗斯大列巴'})
               CREATE (a)-[:NEAR_FOOD {distance: '1.5km', tip: '景区边境贸易店有售俄罗斯传统大列巴'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '土字牌'}), (f:Food {name: '珲春帝王蟹'})
               CREATE (a)-[:NEAR_FOOD {distance: '3km', tip: '界碑附近渔村可预订鲜活帝王蟹盛宴'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '防川风景区'}), (ac:Accommodation {name: '珲春民族花园国际酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '15km', tip: '三国风光游览后可休整，提供帝王蟹特色餐'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '土字牌'}), (ac:Accommodation {name: '珲春宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '18km', tip: '界碑参观后可休整，提供俄式列巴早餐'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '珲春'}), (t:Transportation)
               WHERE t.name IN ['珲春公交', '珲春站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '珲春公交'}), (t2:Transportation {name: '珲春站'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '公交直达火车站，方便前往延吉、长春等地'}]->(t2)
           """)

        print("珲春旅游数据导入完成！")

    def import_longjing_data(self):
        """导入龙井旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (lj:City {name: '龙井', level: '县级市', description: '吉林省县级市，延边州代管，中国苹果梨之乡，朝鲜族发源地'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (longjing_minzubo:Attraction {name: '龙井朝鲜族民俗博物馆', type: '人文景观', rating: 4.5, opening_hours: '9:00-16:30'}),
               (piyan_shan:Attraction {name: '琵岩山风景区', type: '自然景观', rating: 4.4, opening_hours: '8:00-17:00'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (longjing_pingguoli:Food {name: '龙井苹果梨', type: '地方特产', price_range: '低', description: '果肉细腻，酸甜适口'}),
               (michang:Food {name: '米肠', type: '朝鲜族美食', price_range: '中低', description: '软糯咸香，风味独特'}),
               (longjing_binguan:Accommodation {name: '龙井宾馆', type: '三星级', price_range: '中低', rating: 4.3}),
               (longjing_dongshan:Accommodation {name: '龙井东山宾馆', type: '商务酒店', price_range: '中低', rating: 4.2}),
               (longjing_bus:Transportation {name: '龙井公交', type: '公交', route: '覆盖市区', price: '1-2元'}),
               (longjing_zhan:Transportation {name: '龙井站', type: '火车', route: '通往延吉等地', price: '根据里程'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '龙井'})
               WHERE a.name IN ['龙井朝鲜族民俗博物馆', '琵岩山风景区']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '龙井'}), (f:Food)
               WHERE f.name IN ['龙井苹果梨', '米肠']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '龙井朝鲜族民俗博物馆'}), (f:Food {name: '龙井苹果梨'})
               CREATE (a)-[:NEAR_FOOD {distance: '600m', tip: '博物馆外果园可采摘苹果梨，体验鲜果风味'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '龙井朝鲜族民俗博物馆'}), (f:Food {name: '米肠'})
               CREATE (a)-[:NEAR_FOOD {distance: '400m', tip: '博物馆民俗餐厅有现蒸米肠配蒜酱'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '琵岩山风景区'}), (f:Food {name: '龙井苹果梨'})
               CREATE (a)-[:NEAR_FOOD {distance: '1.2km', tip: '山脚下果农直销苹果梨及梨汁饮品'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '龙井朝鲜族民俗博物馆'}), (ac:Accommodation {name: '龙井宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '1km', tip: '文化体验后可休整，提供苹果梨甜品'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '琵岩山风景区'}), (ac:Accommodation {name: '龙井东山宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '2.5km', tip: '山地游览后可休整，提供米肠特色餐'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '龙井'}), (t:Transportation)
               WHERE t.name IN ['龙井公交', '龙井站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '龙井公交'}), (t2:Transportation {name: '龙井站'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '公交直达火车站，方便前往延吉、图们等地'}]->(t2)
           """)

        print("龙井旅游数据导入完成！")

    def import_helong_data(self):
        """导入和龙旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (hl:City {name: '和龙', level: '县级市', description: '吉林省县级市，延边州代管，中朝边境城市，金达莱故乡'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (xianjingtai_fengjingqu:Attraction {name: '仙景台风景区', type: '自然景观', rating: 4.6, opening_hours: '8:00-17:00'}),
               (jindalai_cuncun:Attraction {name: '金达莱民俗村', type: '人文景观', rating: 4.5, opening_hours: '9:00-17:00'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (mingtaiyu:Food {name: '明太鱼', type: '地方特色', price_range: '中低', description: '肉质鲜美，做法多样'}),
               (labaicai:Food {name: '辣白菜', type: '朝鲜族美食', price_range: '低', description: '酸辣爽口，开胃下饭'}),
               (helong_binguan:Accommodation {name: '和龙宾馆', type: '三星级', price_range: '中低', rating: 4.3}),
               (helong_jindalai:Accommodation {name: '和龙金达莱酒店', type: '商务酒店', price_range: '中低', rating: 4.2}),
               (helong_bus:Transportation {name: '和龙公交', type: '公交', route: '覆盖市区', price: '1-2元'}),
               (helong_zhan:Transportation {name: '和龙站', type: '火车', route: '通往延吉等地', price: '根据里程'})
           """)

            # 4. 创建景点→城市关系
            session.run("""
               MATCH (a:Attraction), (c:City {name: '和龙'})
               WHERE a.name IN ['仙景台风景区', '金达莱民俗村']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建城市→推荐美食关系
            session.run("""
               MATCH (c:City {name: '和龙'}), (f:Food)
               WHERE f.name IN ['明太鱼', '辣白菜']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建景点→附近美食关系（根据关联提示）
            session.run("""
               MATCH (a:Attraction {name: '金达莱民俗村'}), (f:Food {name: '明太鱼'})
               CREATE (a)-[:NEAR_FOOD {distance: '500m', tip: '民俗村餐馆有辣炒明太鱼、明太鱼干汤等做法'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '金达莱民俗村'}), (f:Food {name: '辣白菜'})
               CREATE (a)-[:NEAR_FOOD {distance: '300m', tip: '民俗村传统作坊可体验辣白菜制作并品尝'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '仙景台风景区'}), (f:Food {name: '明太鱼'})
               CREATE (a)-[:NEAR_FOOD {distance: '3km', tip: '景区出口餐馆有用明太鱼制作的烧烤和火锅'}]->(f)
           """)

            # 7. 创建景点→附近住宿关系（保持位置顺序）
            session.run("""
               MATCH (a:Attraction {name: '金达莱民俗村'}), (ac:Accommodation {name: '和龙宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '2km', tip: '民俗体验后可休整，提供明太鱼特色餐'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '仙景台风景区'}), (ac:Accommodation {name: '和龙金达莱酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '8km', tip: '山地游览后可休整，提供辣白菜佐餐'}]->(ac)
           """)

            # 8. 创建城市→交通关系及交通换乘关系（保持在第七点之后）
            session.run("""
               MATCH (c:City {name: '和龙'}), (t:Transportation)
               WHERE t.name IN ['和龙公交', '和龙站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)
            session.run("""
               MATCH (t1:Transportation {name: '和龙公交'}), (t2:Transportation {name: '和龙站'})
               CREATE (t1)-[:CAN_TRANSFER_TO {tip: '公交直达火车站，方便前往延吉、龙井等地'}]->(t2)
           """)

        print("和龙旅游数据导入完成！")

    def import_haerbin_data(self):
        """导入哈尔滨旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (heb:City {name: '哈尔滨', level: '新一线城市', description: '中国东北地区中心城市，被誉为“冰城夏都”、“东方莫斯科”'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (suofeiya:Attraction {name: '圣索菲亚大教堂', type: '人文景观', rating: 4.8, opening_hours: '8:30-17:00'}),
               (bingxue:Attraction {name: '哈尔滨冰雪大世界', type: '主题乐园/人文景观', rating: 4.7, opening_hours: '11:00-21:30（随季节调整）'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (guobaorou:Food {name: '锅包肉', type: '东北菜', price_range: '中低', description: '酸甜酥脆'}),
               (madieer:Food {name: '马迭尔冰棍', type: '小吃/冷饮', price_range: '低', description: '奶香浓郁'}),
               (xianggelila:Accommodation {name: '哈尔滨香格里拉', type: '五星级酒店', price_range: '高', rating: 4.7}),
               (madieerhotel:Accommodation {name: '马迭尔宾馆', type: '历史精品酒店', price_range: '中高', rating: 4.6}),
               (ditie2:Transportation {name: '地铁2号线', type: '地铁', route: '江北大学城-气象台', price: '2-6元'}),
               (jichangdaba:Transportation {name: '哈尔滨太平国际机场大巴', type: '大巴', route: '机场-市区', price: '20元'})
           """)

            # 4. 创建关系：景点→城市
            session.run("""
               MATCH (a:Attraction), (c:City {name: '哈尔滨'})
               WHERE a.name IN ['圣索菲亚大教堂', '哈尔滨冰雪大世界']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建关系：城市→推荐美食
            session.run("""
               MATCH (c:City {name: '哈尔滨'}), (f:Food)
               WHERE f.name IN ['锅包肉', '马迭尔冰棍']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建关系：景点→附近美食
            session.run("""
               MATCH (a:Attraction {name: '圣索菲亚大教堂'}), (f:Food {name: '马迭尔冰棍'})
               CREATE (a)-[:NEAR_FOOD {distance: '位于中央大街内'}]->(f)
           """)

            # 7. 创建关系：景点→附近住宿
            session.run("""
               MATCH (a:Attraction {name: '哈尔滨冰雪大世界'}), (ac:Accommodation {name: '哈尔滨香格里拉'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '约4km'}]->(ac)
           """)

            # 8. 创建关系：城市→交通
            session.run("""
               MATCH (c:City {name: '哈尔滨'}), (t:Transportation)
               WHERE t.name IN ['地铁2号线', '哈尔滨太平国际机场大巴']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)

        print("哈尔滨旅游数据导入完成！")

    def import_qiqihaer_data(self):
        """导入齐齐哈尔旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (qqhe:City {name: '齐齐哈尔', level: '三线城市', description: '中国重要的老工业基地，被誉为“鹤城”、“钢铁之城”，丹顶鹤的故乡'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (zalong:Attraction {name: '扎龙自然保护区', type: '自然景观', rating: 4.8, opening_hours: '8:00-16:00'}),
               (longsha:Attraction {name: '龙沙公园', type: '自然+人文景观', rating: 4.6, opening_hours: '全天开放'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (kaorou:Food {name: '齐齐哈尔烤肉', type: '东北菜', price_range: '中', description: '风味独特，肉质鲜美'}),
               (tieguodun:Food {name: '铁锅炖', type: '东北菜', price_range: '中低', description: '汤汁浓郁，暖心暖胃'}),
               (wanda:Accommodation {name: '齐齐哈尔万达嘉华酒店', type: '五星级酒店', price_range: '中高', rating: 4.5}),
               (guomai:Accommodation {name: '齐齐哈尔国脉大厦酒店', type: '商务酒店', price_range: '中', rating: 4.3}),
               (bus3:Transportation {name: '齐齐哈尔3路公交车', type: '公交', route: '火车站-扎龙自然保护区', price: '2-5元'}),
               (airportbus:Transportation {name: '齐齐哈尔三家子机场大巴', type: '大巴', route: '机场-市区', price: '15元'})
           """)

            # 4. 创建关系：景点→城市
            session.run("""
               MATCH (a:Attraction), (c:City {name: '齐齐哈尔'})
               WHERE a.name IN ['扎龙自然保护区', '龙沙公园']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建关系：城市→推荐美食
            session.run("""
               MATCH (c:City {name: '齐齐哈尔'}), (f:Food)
               WHERE f.name IN ['齐齐哈尔烤肉', '铁锅炖']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建关系：景点→附近美食
            session.run("""
               MATCH (a:Attraction {name: '龙沙公园'}), (f:Food {name: '铁锅炖'})
               CREATE (a)-[:NEAR_FOOD {distance: '800米'}]->(f)
           """)

            # 7. 创建关系：景点→附近住宿
            session.run("""
               MATCH (a:Attraction {name: '扎龙自然保护区'}), (ac:Accommodation {name: '齐齐哈尔万达嘉华酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '约15km'}]->(ac)
           """)

            # 8. 创建关系：城市→交通
            session.run("""
               MATCH (c:City {name: '齐齐哈尔'}), (t:Transportation)
               WHERE t.name IN ['齐齐哈尔3路公交车', '齐齐哈尔三家子机场大巴']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)

        print("齐齐哈尔旅游数据导入完成！")

    def import_jixi_data(self):
        """导入鸡西旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (jixi:City {name: '鸡西', level: '五线城市', description: '黑龙江省东部区域性中心城市，被誉为“东北煤城”、“中国石墨之都”，毗邻兴凯湖'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (xingkaihu:Attraction {name: '兴凯湖', type: '自然景观', rating: 4.7, opening_hours: '全天开放'}),
               (beidahuang:Attraction {name: '北大荒书法艺术长廊', type: '人文景观', rating: 4.3, opening_hours: '8:30-16:30'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (lengmian:Food {name: '鸡西冷面', type: '地方特色', price_range: '低', description: '酸甜爽口，风味独特'}),
               (lacai:Food {name: '辣菜', type: '地方特色', price_range: '低', description: '咸香麻辣的拌菜，冷面绝配'}),
               (zhongxin:Accommodation {name: '鸡西中心大厦', type: '商务酒店', price_range: '中', rating: 4.2}),
               (xingkaihubin:Accommodation {name: '兴凯湖宾馆', type: '度假酒店', price_range: '中', rating: 4.0}),
               (gongjiao:Transportation {name: '鸡西公交线网', type: '公交', route: '覆盖市内主要区域', price: '1-2元'}),
               (jixiairportbus:Transportation {name: '兴凯湖机场大巴', type: '大巴', route: '机场-市区', price: '20元'})
           """)

            # 4. 创建关系：景点→城市
            session.run("""
               MATCH (a:Attraction), (c:City {name: '鸡西'})
               WHERE a.name IN ['兴凯湖', '北大荒书法艺术长廊']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建关系：城市→推荐美食
            session.run("""
               MATCH (c:City {name: '鸡西'}), (f:Food)
               WHERE f.name IN ['鸡西冷面', '辣菜']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建关系：景点→附近美食（根据"市区内各处均可方便找到"，关联市区景点与美食）
            session.run("""
               MATCH (a:Attraction {name: '北大荒书法艺术长廊'}), (f:Food)
               WHERE f.name IN ['鸡西冷面', '辣菜']
               CREATE (a)-[:NEAR_FOOD {distance: '市区内可便捷找到'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '兴凯湖'}), (f:Food)
               WHERE f.name IN ['鸡西冷面', '辣菜']
               CREATE (a)-[:NEAR_FOOD {distance: '景区及周边可找到'}]->(f)
           """)

            # 7. 创建关系：景点→附近住宿
            session.run("""
               MATCH (a:Attraction {name: '兴凯湖'}), (ac:Accommodation {name: '兴凯湖宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '位于景区内'}]->(ac)
           """)

            # 8. 创建关系：城市→交通
            session.run("""
               MATCH (c:City {name: '鸡西'}), (t:Transportation)
               WHERE t.name IN ['鸡西公交线网', '兴凯湖机场大巴']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)

        print("鸡西旅游数据导入完成！")

    def import_hegang_data(self):
        """导入鹤岗旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (hegang:City {name: '鹤岗', level: '五线城市', description: '黑龙江省东北部边境城市，被誉为“煤城”，近年来因低房价现象受到全国关注'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (senlingongyuan:Attraction {name: '鹤岗国家森林公园', type: '自然景观', rating: 4.5, opening_hours: '8:30-16:30'}),
               (tianshuihu:Attraction {name: '天水湖公园', type: '自然+人文景观', rating: 4.2, opening_hours: '全天开放'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (xiaochuan:Food {name: '鹤岗小串', type: '地方烧烤', price_range: '低', description: '肉质鲜嫩，口味独特'}),
               (dunjiangyu:Food {name: '炖江鱼', type: '地方菜', price_range: '中低', description: '选用黑龙江野生江鱼，味道鲜美'}),
               (jiuzhou:Accommodation {name: '鹤岗九州国际酒店', type: '商务酒店', price_range: '中', rating: 4.3}),
               (longyun:Accommodation {name: '鹤岗龙运大酒店', type: '商务酒店', price_range: '中低', rating: 4.1}),
               (bus1:Transportation {name: '鹤岗公交1路', type: '公交', route: '覆盖市中心主干道', price: '1-2元'}),
               (keyunzhan:Transportation {name: '鹤岗客运站班车', type: '大巴', route: '连通周边县市', price: '依里程而定'})
           """)

            # 4. 创建关系：景点→城市
            session.run("""
               MATCH (a:Attraction), (c:City {name: '鹤岗'})
               WHERE a.name IN ['鹤岗国家森林公园', '天水湖公园']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建关系：城市→推荐美食
            session.run("""
               MATCH (c:City {name: '鹤岗'}), (f:Food)
               WHERE f.name IN ['鹤岗小串', '炖江鱼']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建关系：景点→附近美食（根据"市区内遍布多家鹤岗小串烧烤店"关联市区景点）
            session.run("""
               MATCH (a:Attraction), (f:Food {name: '鹤岗小串'})
               WHERE a.name IN ['鹤岗国家森林公园', '天水湖公园']
               CREATE (a)-[:NEAR_FOOD {distance: '市区内遍布门店'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction), (f:Food {name: '炖江鱼'})
               WHERE a.name IN ['鹤岗国家森林公园', '天水湖公园']
               CREATE (a)-[:NEAR_FOOD {distance: '市区及周边可找到'}]->(f)
           """)

            # 7. 创建关系：景点→附近住宿
            session.run("""
               MATCH (a:Attraction {name: '鹤岗国家森林公园'}), (ac:Accommodation {name: '鹤岗九州国际酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '约5km'}]->(ac)
           """)

            # 8. 创建关系：城市→交通
            session.run("""
               MATCH (c:City {name: '鹤岗'}), (t:Transportation)
               WHERE t.name IN ['鹤岗公交1路', '鹤岗客运站班车']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)

        print("鹤岗旅游数据导入完成！")

    def import_shuangyashan_data(self):
        """导入双鸭山市旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (sys:City {name: '双鸭山', level: '五线城市', description: '位于黑龙江省东北部，是重要的煤炭工业城市，被誉为“黑土湿地之都”，自然资源丰富'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (beixiu:Attraction {name: '北秀公园', type: '自然+人文景观', rating: 4.4, opening_hours: '全天开放'}),
               (fenglin:Attraction {name: '凤林古城', type: '人文景观', rating: 4.2, opening_hours: '8:30-16:30'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (shazhucai:Food {name: '杀猪菜', type: '东北菜', price_range: '中低', description: '酸菜血肠五花肉，乡土风味浓郁'}),
               (syslengmian:Food {name: '双鸭山冷面', type: '地方特色', price_range: '低', description: '与周边城市风味略有不同的朝鲜族冷面'}),
               (shidaiguangchang:Accommodation {name: '双鸭山时代广场酒店', type: '商务酒店', price_range: '中', rating: 4.2}),
               (yingbinguan:Accommodation {name: '双鸭山迎宾馆', type: '商务酒店', price_range: '中', rating: 4.0}),
               (sysbus:Transportation {name: '双鸭山公交线网', type: '公交', route: '覆盖市内主要区域', price: '1-2元'}),
               (keyunzongzhan:Transportation {name: '双鸭山客运总站班车', type: '大巴', route: '连通哈尔滨及周边县市', price: '依里程而定'})
           """)

            # 4. 创建关系：景点→城市
            session.run("""
               MATCH (a:Attraction), (c:City {name: '双鸭山'})
               WHERE a.name IN ['北秀公园', '凤林古城']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建关系：城市→推荐美食
            session.run("""
               MATCH (c:City {name: '双鸭山'}), (f:Food)
               WHERE f.name IN ['杀猪菜', '双鸭山冷面']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建关系：景点→附近美食
            session.run("""
               MATCH (a:Attraction {name: '北秀公园'}), (f:Food {name: '杀猪菜'})
               CREATE (a)-[:NEAR_FOOD {distance: '1km内'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '北秀公园'}), (f:Food {name: '双鸭山冷面'})
               CREATE (a)-[:NEAR_FOOD {distance: '市区内可找到'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '凤林古城'}), (f:Food)
               WHERE f.name IN ['杀猪菜', '双鸭山冷面']
               CREATE (a)-[:NEAR_FOOD {distance: '周边可找到'}]->(f)
           """)

            # 7. 创建关系：景点→附近住宿
            session.run("""
               MATCH (a:Attraction {name: '凤林古城'}), (ac:Accommodation {name: '双鸭山迎宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '约8km'}]->(ac)
           """)

            # 8. 创建关系：城市→交通
            session.run("""
               MATCH (c:City {name: '双鸭山'}), (t:Transportation)
               WHERE t.name IN ['双鸭山公交线网', '双鸭山客运总站班车']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)

        print("双鸭山市旅游数据导入完成！")

    def import_daqing_data(self):
        """导入大庆市旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (dq:City {name: '大庆', level: '三线城市', description: '中国著名的“油城”、“百湖之城”，是世界著名的石油和化工城市，也是一座现代化的生态园林城市'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (tieren:Attraction {name: '铁人王进喜纪念馆', type: '人文景观/红色旅游', rating: 4.8, opening_hours: '9:00-16:00（周一闭馆）'}),
               (longfeng:Attraction {name: '大庆龙凤湿地', type: '自然景观', rating: 4.6, opening_hours: '9:00-17:00'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (quanyuyan:Food {name: '全鱼宴', type: '地方特色', price_range: '中高', description: '利用湿地淡水鱼烹制的系列菜肴，鲜美无比'}),
               (kengkao:Food {name: '大庆坑烤', type: '地方特色', price_range: '中', description: '用土坑烤制的羊肉、土豆等，外焦里嫩，风味独特'}),
               (wandahilton:Accommodation {name: '大庆万达希尔顿酒店', type: '五星级酒店', price_range: '高', rating: 4.7}),
               (daqingbinguan:Accommodation {name: '大庆宾馆', type: '商务酒店', price_range: '中', rating: 4.4}),
               (brt:Transportation {name: '大庆快速公交（BRT）', type: '快速公交', route: '连接东西城区', price: '1-3元'}),
               (saertu:Transportation {name: '大庆萨尔图机场大巴', type: '大巴', route: '机场-市区', price: '25元'})
           """)

            # 4. 创建关系：景点→城市
            session.run("""
               MATCH (a:Attraction), (c:City {name: '大庆'})
               WHERE a.name IN ['铁人王进喜纪念馆', '大庆龙凤湿地']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建关系：城市→推荐美食
            session.run("""
               MATCH (c:City {name: '大庆'}), (f:Food)
               WHERE f.name IN ['全鱼宴', '大庆坑烤']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建关系：景点→附近美食
            session.run("""
               MATCH (a:Attraction {name: '大庆龙凤湿地'}), (f:Food {name: '全鱼宴'})
               CREATE (a)-[:NEAR_FOOD {distance: '2km内'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '大庆龙凤湿地'}), (f:Food {name: '大庆坑烤'})
               CREATE (a)-[:NEAR_FOOD {distance: '周边可找到'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '铁人王进喜纪念馆'}), (f:Food {name: '大庆坑烤'})
               CREATE (a)-[:NEAR_FOOD {distance: '市区内可找到'}]->(f)
           """)

            # 7. 创建关系：景点→附近住宿
            session.run("""
               MATCH (a:Attraction {name: '铁人王进喜纪念馆'}), (ac:Accommodation {name: '大庆宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '约4km'}]->(ac)
           """)

            # 8. 创建关系：城市→交通
            session.run("""
               MATCH (c:City {name: '大庆'}), (t:Transportation)
               WHERE t.name IN ['大庆快速公交（BRT）', '大庆萨尔图机场大巴']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)

        print("大庆市旅游数据导入完成！")

    def import_jiamusi_data(self):
        """导入佳木斯市旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (jiamusi:City {name: '佳木斯', level: '四线城市', description: '黑龙江省东北部中心城市，被誉为“华夏东极”，是祖国最早迎接太阳的地方，同时也是赫哲族的主要聚居地'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (heixiazi:Attraction {name: '黑瞎子岛', type: '自然+人文景观', rating: 4.5, opening_hours: '8:30-17:00'}),
               (yanjiang:Attraction {name: '佳木斯沿江公园', type: '自然+人文景观', rating: 4.6, opening_hours: '全天开放'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (talaha:Food {name: '赫哲族塔拉哈', type: '民族特色', price_range: '中', description: '用火焰烤制的半生鲜鱼，口感鲜嫩独特'}),
               (banmian:Food {name: '佳木斯拌面', type: '地方特色', price_range: '低', description: '酸甜咸辣口味均衡的朝鲜族冷面'}),
               (guojifandian:Accommodation {name: '佳木斯国际饭店', type: '商务酒店', price_range: '中', rating: 4.4}),
               (jiangtianbinguan:Accommodation {name: '佳木斯江天宾馆', type: '商务酒店', price_range: '中', rating: 4.2}),
               (jiamusibus:Transportation {name: '佳木斯公交线网', type: '公交', route: '覆盖市内及近郊', price: '1-2元'}),
               (dongjiaojichang:Transportation {name: '佳木斯东郊机场大巴', type: '大巴', route: '机场-市区', price: '20元'})
           """)

            # 4. 创建关系：景点→城市
            session.run("""
               MATCH (a:Attraction), (c:City {name: '佳木斯'})
               WHERE a.name IN ['黑瞎子岛', '佳木斯沿江公园']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建关系：城市→推荐美食
            session.run("""
               MATCH (c:City {name: '佳木斯'}), (f:Food)
               WHERE f.name IN ['赫哲族塔拉哈', '佳木斯拌面']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建关系：景点→附近美食
            session.run("""
               MATCH (a:Attraction {name: '佳木斯沿江公园'}), (f:Food {name: '佳木斯拌面'})
               CREATE (a)-[:NEAR_FOOD {distance: '500米内'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '佳木斯沿江公园'}), (f:Food {name: '赫哲族塔拉哈'})
               CREATE (a)-[:NEAR_FOOD {distance: '市区内可找到'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '黑瞎子岛'}), (f:Food)
               WHERE f.name IN ['赫哲族塔拉哈', '佳木斯拌面']
               CREATE (a)-[:NEAR_FOOD {distance: '需返回市区品尝'}]->(f)
           """)

            # 7. 创建关系：景点→附近住宿
            session.run("""
               MATCH (a:Attraction {name: '黑瞎子岛'}), (ac:Accommodation)
               WHERE ac.name IN ['佳木斯国际饭店', '佳木斯江天宾馆']
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '需返回市区或抚远市'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '佳木斯沿江公园'}), (ac:Accommodation)
               WHERE ac.name IN ['佳木斯国际饭店', '佳木斯江天宾馆']
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '市区内较近'}]->(ac)
           """)

            # 8. 创建关系：城市→交通
            session.run("""
               MATCH (c:City {name: '佳木斯'}), (t:Transportation)
               WHERE t.name IN ['佳木斯公交线网', '佳木斯东郊机场大巴']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)

        print("佳木斯市旅游数据导入完成！")

    def import_yichun_data(self):
        """导入伊春市旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (yichun:City {name: '伊春', level: '五线城市', description: '地处黑龙江省东北部的小兴安岭腹地，被誉为“中国林都”、“红松故乡”，是一座天然的森林氧吧'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (wuying:Attraction {name: '五营国家森林公园', type: '自然景观', rating: 4.7, opening_hours: '8:00-17:00'}),
               (tangwanghe:Attraction {name: '汤旺河林海奇石景区', type: '自然景观', rating: 4.6, opening_hours: '8:30-17:00'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (lanmeiguojiu:Food {name: '蓝莓果酒', type: '地方特产', price_range: '中', description: '采用小兴安岭野生蓝莓酿造，口感醇厚'}),
               (senlinyan:Food {name: '森林宴', type: '地方特色', price_range: '中', description: '以林区特有的蘑菇、野菜、野果等为食材'}),
               (baoyulonghua:Accommodation {name: '伊春宝宇龙花温泉酒店', type: '度假酒店', price_range: '中高', rating: 4.5}),
               (qingnianyizhan:Accommodation {name: '伊春青年驿站', type: '经济型酒店', price_range: '低', rating: 4.3}),
               (lvyoudaxian:Transportation {name: '伊春旅游专线大巴', type: '旅游巴士', route: '市区-各主要森林公园', price: '10-30元'}),
               (lindujichang:Transportation {name: '伊春林都机场大巴', type: '大巴', route: '机场-市区', price: '15元'})
           """)

            # 4. 创建关系：景点→城市
            session.run("""
               MATCH (a:Attraction), (c:City {name: '伊春'})
               WHERE a.name IN ['五营国家森林公园', '汤旺河林海奇石景区']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建关系：城市→推荐美食
            session.run("""
               MATCH (c:City {name: '伊春'}), (f:Food)
               WHERE f.name IN ['蓝莓果酒', '森林宴']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建关系：景点→附近美食
            session.run("""
               MATCH (a:Attraction), (f:Food)
               WHERE a.name IN ['五营国家森林公园', '汤旺河林海奇石景区']
                 AND f.name IN ['蓝莓果酒', '森林宴']
               CREATE (a)-[:NEAR_FOOD {distance: '景区周边可找到'}]->(f)
           """)

            # 7. 创建关系：景点→附近住宿
            session.run("""
               MATCH (a:Attraction {name: '五营国家森林公园'}), (ac:Accommodation {name: '伊春宝宇龙花温泉酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '约20km'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '汤旺河林海奇石景区'}), (ac:Accommodation)
               WHERE ac.name IN ['伊春宝宇龙花温泉酒店', '伊春青年驿站']
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '需前往市区或周边'}]->(ac)
           """)

            # 8. 创建关系：城市→交通
            session.run("""
               MATCH (c:City {name: '伊春'}), (t:Transportation)
               WHERE t.name IN ['伊春旅游专线大巴', '伊春林都机场大巴']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)

        print("伊春市旅游数据导入完成！")

    def import_qitaihe_data(self):
        """导入七台河市旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (qitaihe:City {name: '七台河', level: '五线城市', description: '黑龙江省东部城市，以煤炭工业闻名，同时是“国家重点高水平体育后备人才基地”，被誉为“冬奥冠军之乡”，培养了杨扬、王濛等多位短道速滑世界冠军'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (shilongshan:Attraction {name: '石龙山国家森林公园', type: '自然景观', rating: 4.4, opening_hours: '8:00-17:00'}),
               (taoshanhu:Attraction {name: '桃山湖', type: '自然景观', rating: 4.3, opening_hours: '全天开放'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (shaokao:Food {name: '七台河烧烤', type: '地方特色', price_range: '中低', description: '具有地方特色的烤串，风味浓郁'}),
               (suanCaitang:Food {name: '酸菜汤', type: '东北菜', price_range: '低', description: '开胃暖身，家常风味'}),
               (kunlun:Accommodation {name: '七台河昆仑酒店', type: '商务酒店', price_range: '中', rating: 4.3}),
               (jinqiao:Accommodation {name: '七台河金桥酒店', type: '商务酒店', price_range: '中低', rating: 4.1}),
               (qitaihebus:Transportation {name: '七台河市内公交', type: '公交', route: '覆盖主要城区', price: '1-2元'}),
               (qitaihekeyun:Transportation {name: '七台河客运站班车', type: '大巴', route: '连通哈尔滨、佳木斯等周边城市', price: '依里程而定'})
           """)

            # 4. 创建关系：景点→城市
            session.run("""
               MATCH (a:Attraction), (c:City {name: '七台河'})
               WHERE a.name IN ['石龙山国家森林公园', '桃山湖']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建关系：城市→推荐美食
            session.run("""
               MATCH (c:City {name: '七台河'}), (f:Food)
               WHERE f.name IN ['七台河烧烤', '酸菜汤']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建关系：景点→附近美食
            session.run("""
               MATCH (a:Attraction), (f:Food {name: '七台河烧烤'})
               WHERE a.name IN ['石龙山国家森林公园', '桃山湖']
               CREATE (a)-[:NEAR_FOOD {distance: '市区内遍布门店'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction), (f:Food {name: '酸菜汤'})
               WHERE a.name IN ['石龙山国家森林公园', '桃山湖']
               CREATE (a)-[:NEAR_FOOD {distance: '市区及周边可找到'}]->(f)
           """)

            # 7. 创建关系：景点→附近住宿
            session.run("""
               MATCH (a:Attraction {name: '石龙山国家森林公园'}), (ac:Accommodation {name: '七台河昆仑酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '约6km'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '桃山湖'}), (ac:Accommodation)
               WHERE ac.name IN ['七台河昆仑酒店', '七台河金桥酒店']
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '市区内较近'}]->(ac)
           """)

            # 8. 创建关系：城市→交通
            session.run("""
               MATCH (c:City {name: '七台河'}), (t:Transportation)
               WHERE t.name IN ['七台河市内公交', '七台河客运站班车']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)

        print("七台河市旅游数据导入完成！")

    def import_mudanjiang_data(self):
        """导入牡丹江市旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (mudanjiang:City {name: '牡丹江', level: '四线城市', description: '黑龙江省东南部重要的区域性中心城市，被誉为“雪城”，是通往镜泊湖、雪乡等著名景区的旅游集散中心'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (jingpohu:Attraction {name: '镜泊湖', type: '自然景观', rating: 4.8, opening_hours: '全天开放（景点单独开放）'}),
               (xuexiang:Attraction {name: '中国雪乡', type: '自然+人文景观', rating: 4.5, opening_hours: '全天开放（最佳观赏期为冬季）'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (jingpohuyuyan:Food {name: '镜泊湖鱼宴', type: '地方特色', price_range: '中高', description: '以镜泊湖盛产的湖鱼烹制，味道鲜美'}),
               (chaoxianzu冷面:Food {name: '朝鲜族大冷面', type: '民族特色', price_range: '低', description: '酸甜冰爽，口感筋道'}),
               (shimao:Accommodation {name: '牡丹江世茂假日酒店', type: '高端酒店', price_range: '中高', rating: 4.6}),
               (baihuo:Accommodation {name: '牡丹江百货大楼宾馆', type: '商务酒店', price_range: '中', rating: 4.3}),
               (mudanjiangbus:Transportation {name: '牡丹江公交线网', type: '公交', route: '覆盖市区及近郊', price: '1-2元'}),
               (hailangjichang:Transportation {name: '牡丹江海浪机场大巴', type: '大巴', route: '机场-市区', price: '20元'})
           """)

            # 4. 创建关系：景点→城市
            session.run("""
               MATCH (a:Attraction), (c:City {name: '牡丹江'})
               WHERE a.name IN ['镜泊湖', '中国雪乡']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建关系：城市→推荐美食
            session.run("""
               MATCH (c:City {name: '牡丹江'}), (f:Food)
               WHERE f.name IN ['镜泊湖鱼宴', '朝鲜族大冷面']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建关系：景点→附近美食
            session.run("""
               MATCH (a:Attraction {name: '镜泊湖'}), (f:Food {name: '镜泊湖鱼宴'})
               CREATE (a)-[:NEAR_FOOD {distance: '位于景区内'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '镜泊湖'}), (f:Food {name: '朝鲜族大冷面'})
               CREATE (a)-[:NEAR_FOOD {distance: '景区周边可找到'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '中国雪乡'}), (f:Food)
               WHERE f.name IN ['镜泊湖鱼宴', '朝鲜族大冷面']
               CREATE (a)-[:NEAR_FOOD {distance: '景区内及周边餐馆可提供'}]->(f)
           """)

            # 7. 创建关系：景点→附近住宿
            session.run("""
               MATCH (a:Attraction {name: '中国雪乡'}), (ac:Accommodation)
               WHERE ac.name IN ['牡丹江世茂假日酒店', '牡丹江百货大楼宾馆']
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '需预订景区内的特色民宿或酒店'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '镜泊湖'}), (ac:Accommodation)
               WHERE ac.name IN ['牡丹江世茂假日酒店', '牡丹江百货大楼宾馆']
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '景区内及周边有住宿选择'}]->(ac)
           """)

            # 8. 创建关系：城市→交通
            session.run("""
               MATCH (c:City {name: '牡丹江'}), (t:Transportation)
               WHERE t.name IN ['牡丹江公交线网', '牡丹江海浪机场大巴']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)

        print("牡丹江市旅游数据导入完成！")

    def import_heihe_data(self):
        """导入黑河市旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (heihe:City {name: '黑河', level: '五线城市', description: '中国北部边境口岸城市，与俄罗斯布拉戈维申斯克市隔江相望，被誉为“中俄之窗”、“欧亚之门”，拥有独特的异域风情'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (wudalianchi:Attraction {name: '五大连池风景区', type: '自然景观', rating: 4.8, opening_hours: '全天开放（各景点不同）'}),
               (zhongeminfeng:Attraction {name: '中俄民族风情园', type: '人文景观', rating: 4.4, opening_hours: '8:30-17:00'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (eshixi:Food {name: '俄式西餐', type: '异国风味', price_range: '中', description: '红菜汤、大列巴等，口味正宗'}),
               (lengshuiyuyan:Food {name: '冷水鱼宴', type: '地方特色', price_range: '中', description: '以黑龙江特产鲟鳇鱼等为食材，鲜美无比'}),
               (yinjianjianguo:Accommodation {name: '黑河银建建国酒店', type: '商务酒店', price_range: '中', rating: 4.4}),
               (guoijifandian:Accommodation {name: '黑河国际饭店', type: '商务酒店', price_range: '中', rating: 4.2}),
               (heihebus:Transportation {name: '黑河公交线网', type: '公交', route: '覆盖市内主要区域', price: '1-2元'}),
               (kouanbus:Transportation {name: '黑河口岸直通大巴', type: '大巴', route: '黑河-布拉戈维申斯克（俄罗斯）', price: '约50元'})
           """)

            # 4. 创建关系：景点→城市
            session.run("""
               MATCH (a:Attraction), (c:City {name: '黑河'})
               WHERE a.name IN ['五大连池风景区', '中俄民族风情园']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建关系：城市→推荐美食
            session.run("""
               MATCH (c:City {name: '黑河'}), (f:Food)
               WHERE f.name IN ['俄式西餐', '冷水鱼宴']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建关系：景点→附近美食
            session.run("""
               MATCH (a:Attraction {name: '中俄民族风情园'}), (f:Food {name: '俄式西餐'})
               CREATE (a)-[:NEAR_FOOD {distance: '园区内及附近'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '中俄民族风情园'}), (f:Food {name: '冷水鱼宴'})
               CREATE (a)-[:NEAR_FOOD {distance: '市区内可找到'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '五大连池风景区'}), (f:Food)
               WHERE f.name IN ['俄式西餐', '冷水鱼宴']
               CREATE (a)-[:NEAR_FOOD {distance: '景区内及周边可提供'}]->(f)
           """)

            # 7. 创建关系：景点→附近住宿
            session.run("""
               MATCH (a:Attraction {name: '五大连池风景区'}), (ac:Accommodation)
               WHERE ac.name IN ['黑河银建建国酒店', '黑河国际饭店']
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '需预订景区内的酒店或返回市区'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '中俄民族风情园'}), (ac:Accommodation)
               WHERE ac.name IN ['黑河银建建国酒店', '黑河国际饭店']
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '市区内住宿便利'}]->(ac)
           """)

            # 8. 创建关系：城市→交通
            session.run("""
               MATCH (c:City {name: '黑河'}), (t:Transportation)
               WHERE t.name IN ['黑河公交线网', '黑河口岸直通大巴']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)

        print("黑河市旅游数据导入完成！")

    def import_suihua_data(self):
        """导入绥化市旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (suihua:City {name: '绥化', level: '五线城市', description: '位于黑龙江省中部，是重要的寒地黑土农业区，被誉为“塞北江南”、“北大荒的粮仓”，以绿色农产品闻名'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (jinguishanzhuang:Attraction {name: '金龟山庄', type: '自然+人文景观', rating: 4.3, opening_hours: '8:00-17:00'}),
               (linfengguju:Attraction {name: '林枫故居纪念馆', type: '人文景观/红色旅游', rating: 4.2, opening_hours: '9:00-16:00'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (kaolengmian:Food {name: '绥化烤冷面', type: '地方小吃', price_range: '低', description: '烤制而成，与常见的油炸冷面口感不同'}),
               (nongjiashazhucai:Food {name: '农家杀猪菜', type: '东北菜', price_range: '中低', description: '采用本地黑猪肉，味道纯正'}),
               (zhongmengkaiyue:Accommodation {name: '绥化中盟凯悦酒店', type: '商务酒店', price_range: '中', rating: 4.3}),
               (huachenshangwu:Accommodation {name: '绥化华辰商务酒店', type: '商务酒店', price_range: '中低', rating: 4.1}),
               (suihuabus:Transportation {name: '绥化市内公交', type: '公交', route: '覆盖主要城区', price: '1-2元'}),
               (gonglukeyun:Transportation {name: '绥化公路客运总站班车', type: '大巴', route: '连通哈尔滨及下属各县市', price: '依里程而定'})
           """)

            # 4. 创建关系：景点→城市
            session.run("""
               MATCH (a:Attraction), (c:City {name: '绥化'})
               WHERE a.name IN ['金龟山庄', '林枫故居纪念馆']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建关系：城市→推荐美食
            session.run("""
               MATCH (c:City {name: '绥化'}), (f:Food)
               WHERE f.name IN ['绥化烤冷面', '农家杀猪菜']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建关系：景点→附近美食
            session.run("""
               MATCH (a:Attraction), (f:Food)
               WHERE a.name IN ['金龟山庄', '林枫故居纪念馆']
                 AND f.name IN ['绥化烤冷面', '农家杀猪菜']
               CREATE (a)-[:NEAR_FOOD {distance: '市区内可方便找到'}]->(f)
           """)

            # 7. 创建关系：景点→附近住宿
            session.run("""
               MATCH (a:Attraction {name: '金龟山庄'}), (ac:Accommodation)
               WHERE ac.name IN ['绥化中盟凯悦酒店', '绥化华辰商务酒店']
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '需返回市区'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '林枫故居纪念馆'}), (ac:Accommodation)
               WHERE ac.name IN ['绥化中盟凯悦酒店', '绥化华辰商务酒店']
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '市区内住宿便利'}]->(ac)
           """)

            # 8. 创建关系：城市→交通
            session.run("""
               MATCH (c:City {name: '绥化'}), (t:Transportation)
               WHERE t.name IN ['绥化市内公交', '绥化公路客运总站班车']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)

        print("绥化市旅游数据导入完成！")

    def import_shangzhi_data(self):
        """导入尚志市旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (shangzhi:City {name: '尚志', level: '县级市', description: '黑龙江省哈尔滨市代管的县级市，以抗日英雄赵尚志的名字命名，是“中国雪都”和“红色旅游名城”，拥有亚布力等著名滑雪胜地'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (yabuli:Attraction {name: '亚布力滑雪旅游度假区', type: '自然+人文景观', rating: 4.7, opening_hours: '全天开放（雪季8:00-16:00）'}),
               (zhaoshangzhi:Attraction {name: '赵尚志纪念馆', type: '人文景观/红色旅游', rating: 4.5, opening_hours: '9:00-16:00（周一闭馆）'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (shanyecai:Food {name: '山野菜', type: '地方特色', price_range: '中低', description: '蕨菜、刺老芽等，清新爽口'}),
               (nongjiayiguochu:Food {name: '农家一锅出', type: '东北菜', price_range: '中低', description: '主食与菜肴一锅炖煮，风味十足'}),
               (yabulinsen:Accommodation {name: '亚布力森林温泉酒店', type: '度假酒店', price_range: '高', rating: 4.6}),
               (shangzhibinguan:Accommodation {name: '尚志市宾馆', type: '商务酒店', price_range: '中', rating: 4.2}),
               (yabulibus:Transportation {name: '亚布力南站旅游巴士', type: '旅游巴士', route: '亚布力南站-滑雪度假区', price: '5-10元'}),
               (shangzhikeyun:Transportation {name: '尚志市客运站班车', type: '大巴', route: '连通哈尔滨及周边市县', price: '依里程而定'})
           """)

            # 4. 创建关系：景点→城市
            session.run("""
               MATCH (a:Attraction), (c:City {name: '尚志'})
               WHERE a.name IN ['亚布力滑雪旅游度假区', '赵尚志纪念馆']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建关系：城市→推荐美食
            session.run("""
               MATCH (c:City {name: '尚志'}), (f:Food)
               WHERE f.name IN ['山野菜', '农家一锅出']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建关系：景点→附近美食
            session.run("""
               MATCH (a:Attraction {name: '亚布力滑雪旅游度假区'}), (f:Food {name: '山野菜'})
               CREATE (a)-[:NEAR_FOOD {distance: '度假区内有多家餐厅提供'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '亚布力滑雪旅游度假区'}), (f:Food {name: '农家一锅出'})
               CREATE (a)-[:NEAR_FOOD {distance: '度假区及周边可找到'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '赵尚志纪念馆'}), (f:Food)
               WHERE f.name IN ['山野菜', '农家一锅出']
               CREATE (a)-[:NEAR_FOOD {distance: '市区内餐馆可提供'}]->(f)
           """)

            # 7. 创建关系：景点→附近住宿
            session.run("""
               MATCH (a:Attraction {name: '亚布力滑雪旅游度假区'}), (ac:Accommodation {name: '亚布力森林温泉酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '位于度假区内'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '赵尚志纪念馆'}), (ac:Accommodation {name: '尚志市宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '市区内较近'}]->(ac)
           """)

            # 8. 创建关系：城市→交通
            session.run("""
               MATCH (c:City {name: '尚志'}), (t:Transportation)
               WHERE t.name IN ['亚布力南站旅游巴士', '尚志市客运站班车']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)

        print("尚志市旅游数据导入完成！")

    def import_wuchang_data(self):
        """导入五常市旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (wuchang:City {name: '五常', level: '县级市', description: '黑龙江省哈尔滨市代管的县级市，被誉为“中国优质稻米之乡”，其出产的“五常大米”闻名全国，是张广才岭下的“鱼米之乡”'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (fenghuangshan:Attraction {name: '凤凰山国家森林公园', type: '自然景观', rating: 4.6, opening_hours: '8:00-17:00'}),
               (daohuaxiang:Attraction {name: '稻花香生态旅游区', type: '自然+农业景观', rating: 4.4, opening_hours: '全天开放（最佳观赏期为夏秋季）'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (damifan:Food {name: '五常大米饭', type: '地方特产', price_range: '中', description: '米香浓郁，口感软糯，空口吃都香甜'}),
               (damiyan:Food {name: '大米宴', type: '地方特色', price_range: '中', description: '以大米为主料或辅料制作的各种创新菜肴'}),
               (jinfu:Accommodation {name: '五常金福大酒店', type: '商务酒店', price_range: '中', rating: 4.3}),
               (fenghuangminsu:Accommodation {name: '凤凰山民宿', type: '民宿', price_range: '中低', rating: 4.5}),
               (wuchangbus:Transportation {name: '五常市内公交', type: '公交', route: '覆盖城区', price: '1-2元'}),
               (wuchangkeyun:Transportation {name: '五常客运站班车', type: '大巴', route: '主要通往哈尔滨及周边', price: '依里程而定'})
           """)

            # 4. 创建关系：景点→城市
            session.run("""
               MATCH (a:Attraction), (c:City {name: '五常'})
               WHERE a.name IN ['凤凰山国家森林公园', '稻花香生态旅游区']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建关系：城市→推荐美食
            session.run("""
               MATCH (c:City {name: '五常'}), (f:Food)
               WHERE f.name IN ['五常大米饭', '大米宴']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建关系：景点→附近美食
            session.run("""
               MATCH (a:Attraction {name: '稻花香生态旅游区'}), (f:Food)
               WHERE f.name IN ['五常大米饭', '大米宴']
               CREATE (a)-[:NEAR_FOOD {distance: '可体验和品尝正宗五常大米相关美食'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '凤凰山国家森林公园'}), (f:Food)
               WHERE f.name IN ['五常大米饭', '大米宴']
               CREATE (a)-[:NEAR_FOOD {distance: '景区及周边餐馆可提供'}]->(f)
           """)

            # 7. 创建关系：景点→附近住宿
            session.run("""
               MATCH (a:Attraction {name: '凤凰山国家森林公园'}), (ac:Accommodation {name: '凤凰山民宿'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '位于景区附近'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '稻花香生态旅游区'}), (ac:Accommodation {name: '五常金福大酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '市区住宿便利'}]->(ac)
           """)

            # 8. 创建关系：城市→交通
            session.run("""
               MATCH (c:City {name: '五常'}), (t:Transportation)
               WHERE t.name IN ['五常市内公交', '五常客运站班车']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)

        print("五常市旅游数据导入完成！")

    def import_hulin_data(self):
        """导入虎林市旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (hulin:City {name: '虎林', level: '县级市', description: '黑龙江省鸡西市代管的县级市，位于黑龙江省东部的乌苏里江畔，是“北大荒精神”的发源地之一，被誉为“英雄的城市，绿色的宝库”'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (hutou:Attraction {name: '虎头旅游风景区', type: '自然+人文景观', rating: 4.7, opening_hours: '8:00-17:00',
                   sub_attractions: ['虎头要塞', '乌苏里江起点', '天下第一虎']}),
               (shendingfeng:Attraction {name: '神顶峰', type: '自然景观', rating: 4.5, opening_hours: '全天开放（建议白天游览）'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (wusulijiangyuyan:Food {name: '乌苏里江鱼宴', type: '地方特色', price_range: '中', description: '“三花五罗”等珍稀江鱼，味道极为鲜美'}),
               (yeshengfengmi:Food {name: '野生蜂蜜', type: '地方特产', price_range: '中低', description: '产自完达山深处，品质纯正'}),
               (dongfang:Accommodation {name: '虎林东方宾馆', type: '商务酒店', price_range: '中', rating: 4.3}),
               (hutouzhen:Accommodation {name: '虎头镇家庭旅馆', type: '民宿', price_range: '低', rating: 4.4}),
               (hulinbus:Transportation {name: '虎林市内公交', type: '公交', route: '覆盖城区', price: '1-2元'}),
               (hulin2hutou:Transportation {name: '虎林至虎头旅游班车', type: '旅游班车', route: '虎林市区-虎头风景区', price: '约15元'})
           """)

            # 4. 创建关系：景点→城市
            session.run("""
               MATCH (a:Attraction), (c:City {name: '虎林'})
               WHERE a.name IN ['虎头旅游风景区', '神顶峰']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建关系：城市→推荐美食
            session.run("""
               MATCH (c:City {name: '虎林'}), (f:Food)
               WHERE f.name IN ['乌苏里江鱼宴', '野生蜂蜜']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建关系：景点→附近美食
            session.run("""
               MATCH (a:Attraction {name: '虎头旅游风景区'}), (f:Food {name: '乌苏里江鱼宴'})
               CREATE (a)-[:NEAR_FOOD {distance: '景区周边江鱼馆可提供'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '虎头旅游风景区'}), (f:Food {name: '野生蜂蜜'})
               CREATE (a)-[:NEAR_FOOD {distance: '景区及周边可购买'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '神顶峰'}), (f:Food)
               WHERE f.name IN ['乌苏里江鱼宴', '野生蜂蜜']
               CREATE (a)-[:NEAR_FOOD {distance: '需前往虎头镇或市区品尝'}]->(f)
           """)

            # 7. 创建关系：景点→附近住宿
            session.run("""
               MATCH (a:Attraction {name: '虎头旅游风景区'}), (ac:Accommodation {name: '虎头镇家庭旅馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '位于景区内'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '神顶峰'}), (ac:Accommodation)
               WHERE ac.name IN ['虎林东方宾馆', '虎头镇家庭旅馆']
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '建议住宿虎头镇或市区'}]->(ac)
           """)

            # 8. 创建关系：城市→交通
            session.run("""
               MATCH (c:City {name: '虎林'}), (t:Transportation)
               WHERE t.name IN ['虎林市内公交', '虎林至虎头旅游班车']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)

        print("虎林市旅游数据导入完成！")

    def import_nehe_data(self):
        """导入讷河市旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (nehe:City {name: '讷河', level: '县级市', description: '黑龙江省齐齐哈尔市代管的县级市，位于松嫩平原北端，素有“北国粮仓”之称，是重要的商品粮基地，以马铃薯闻名'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (yuting:Attraction {name: '雨亭国家城市湿地公园', type: '自然景观', rating: 4.3, opening_hours: '全天开放'}),
               (erzhan:Attraction {name: '讷河尔站生态园', type: '自然+农业观光', rating: 4.1, opening_hours: '8:00-17:00'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (malingshuyan:Food {name: '讷河马铃薯宴', type: '地方特色', price_range: '中低', description: '以优质马铃薯为原料制作的各种创意菜肴'}),
               (jiangyuyan:Food {name: '江鱼宴', type: '地方特色', price_range: '中', description: '选用嫩江野生鱼类，烹饪手法多样'}),
               (huaqi:Accommodation {name: '讷河华旗宾馆', type: '商务酒店', price_range: '中', rating: 4.2}),
               (zhengfuzhaodai:Accommodation {name: '讷河政府招待所', type: '经济型酒店', price_range: '低', rating: 4.0}),
               (nehebus:Transportation {name: '讷河市内公交', type: '公交', route: '覆盖城区', price: '1-2元'}),
               (nehekeyun:Transportation {name: '讷河客运站班车', type: '大巴', route: '连通齐齐哈尔、哈尔滨等地', price: '依里程而定'})
           """)

            # 4. 创建关系：景点→城市
            session.run("""
               MATCH (a:Attraction), (c:City {name: '讷河'})
               WHERE a.name IN ['雨亭国家城市湿地公园', '讷河尔站生态园']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建关系：城市→推荐美食
            session.run("""
               MATCH (c:City {name: '讷河'}), (f:Food)
               WHERE f.name IN ['讷河马铃薯宴', '江鱼宴']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建关系：景点→附近美食
            session.run("""
               MATCH (a:Attraction {name: '雨亭国家城市湿地公园'}), (f:Food {name: '江鱼宴'})
               CREATE (a)-[:NEAR_FOOD {distance: '附近可品尝到地道江鱼'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '雨亭国家城市湿地公园'}), (f:Food {name: '讷河马铃薯宴'})
               CREATE (a)-[:NEAR_FOOD {distance: '市区内可找到'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '讷河尔站生态园'}), (f:Food)
               WHERE f.name IN ['讷河马铃薯宴', '江鱼宴']
               CREATE (a)-[:NEAR_FOOD {distance: '周边及市区可找到'}]->(f)
           """)

            # 7. 创建关系：景点→附近住宿
            session.run("""
               MATCH (a:Attraction {name: '讷河尔站生态园'}), (ac:Accommodation)
               WHERE ac.name IN ['讷河华旗宾馆', '讷河政府招待所']
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '需返回市区'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '雨亭国家城市湿地公园'}), (ac:Accommodation)
               WHERE ac.name IN ['讷河华旗宾馆', '讷河政府招待所']
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '市区内住宿便利'}]->(ac)
           """)

            # 8. 创建关系：城市→交通
            session.run("""
               MATCH (c:City {name: '讷河'}), (t:Transportation)
               WHERE t.name IN ['讷河市内公交', '讷河客运站班车']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)

        print("讷河市旅游数据导入完成！")

    def import_mishan_data(self):
        """导入密山市旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (mishan:City {name: '密山', level: '县级市', description: '黑龙江省鸡西市代管的县级市，位于中俄边境，因境内蜂蜜山而得名。是“北大荒精神”的发源地之一，拥有著名的兴凯湖'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (xingkaihu:Attraction {name: '兴凯湖新开流景区', type: '自然景观', rating: 4.7, opening_hours: '全天开放'}),
               (shufachanglang:Attraction {name: '北大荒书法长廊', type: '人文景观', rating: 4.4, opening_hours: '8:30-16:30'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (dabaiyuyan:Food {name: '兴凯湖大白鱼宴', type: '地方特色', price_range: '中高', description: '清朝贡品，肉质细腻，味道极鲜'}),
               (kaolengmian:Food {name: '烤冷面', type: '地方小吃', price_range: '低', description: '地方特色明显，风味独特'}),
               (jingudasha:Accommodation {name: '密山金谷大厦', type: '商务酒店', price_range: '中', rating: 4.3}),
               (xingkaihubinguan:Accommodation {name: '兴凯湖宾馆', type: '度假酒店', price_range: '中', rating: 4.2}),
               (mishanbus:Transportation {name: '密山市区公交', type: '公交', route: '覆盖城区', price: '1-2元'}),
               (mishan2xingkaihu:Transportation {name: '密山至兴凯湖班车', type: '旅游班车', route: '市区-兴凯湖景区', price: '10-20元'})
           """)

            # 4. 创建关系：景点→城市
            session.run("""
               MATCH (a:Attraction), (c:City {name: '密山'})
               WHERE a.name IN ['兴凯湖新开流景区', '北大荒书法长廊']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建关系：城市→推荐美食
            session.run("""
               MATCH (c:City {name: '密山'}), (f:Food)
               WHERE f.name IN ['兴凯湖大白鱼宴', '烤冷面']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建关系：景点→附近美食
            session.run("""
               MATCH (a:Attraction {name: '兴凯湖新开流景区'}), (f:Food {name: '兴凯湖大白鱼宴'})
               CREATE (a)-[:NEAR_FOOD {distance: '景区周边鱼馆可提供'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '兴凯湖新开流景区'}), (f:Food {name: '烤冷面'})
               CREATE (a)-[:NEAR_FOOD {distance: '景区及市区可找到'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '北大荒书法长廊'}), (f:Food)
               WHERE f.name IN ['兴凯湖大白鱼宴', '烤冷面']
               CREATE (a)-[:NEAR_FOOD {distance: '市区内可找到'}]->(f)
           """)

            # 7. 创建关系：景点→附近住宿
            session.run("""
               MATCH (a:Attraction {name: '兴凯湖新开流景区'}), (ac:Accommodation {name: '兴凯湖宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '位于景区内'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '北大荒书法长廊'}), (ac:Accommodation {name: '密山金谷大厦'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '市区内较近'}]->(ac)
           """)

            # 8. 创建关系：城市→交通
            session.run("""
               MATCH (c:City {name: '密山'}), (t:Transportation)
               WHERE t.name IN ['密山市区公交', '密山至兴凯湖班车']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)

        print("密山市旅游数据导入完成！")

    def import_tieli_data(self):
        """导入铁力市旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (tieli:City {name: '铁力', level: '县级市', description: '黑龙江省伊春市代管的县级市，位于小兴安岭南麓，是进入小兴安岭的重要门户，被誉为“林都门户”、“红松故乡”'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (riyuexia:Attraction {name: '日月峡国家森林公园', type: '自然景观', rating: 4.6, opening_hours: '8:00-17:00'}),
               (taoshan:Attraction {name: '桃山国际狩猎场', type: '自然+体验景观', rating: 4.4, opening_hours: '8:30-16:30'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (shan野菜:Food {name: '林区山野菜', type: '地方特色', price_range: '中低', description: '刺五加、蕨菜等，绿色健康'}),
               (songzi:Food {name: '松子', type: '地方特产', price_range: '中', description: '小兴安岭红松子，香脆可口'}),
               (yuxiang:Accommodation {name: '铁力宇祥国际酒店', type: '商务酒店', price_range: '中', rating: 4.4}),
               (taoshanbinguan:Accommodation {name: '桃山宾馆', type: '度假酒店', price_range: '中', rating: 4.2}),
               (tielibus:Transportation {name: '铁力市区公交', type: '公交', route: '覆盖城区', price: '1-2元'}),
               (tielikeyun:Transportation {name: '铁力客运站班车', type: '大巴', route: '连通哈尔滨、伊春等地', price: '依里程而定'})
           """)

            # 4. 创建关系：景点→城市
            session.run("""
               MATCH (a:Attraction), (c:City {name: '铁力'})
               WHERE a.name IN ['日月峡国家森林公园', '桃山国际狩猎场']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建关系：城市→推荐美食
            session.run("""
               MATCH (c:City {name: '铁力'}), (f:Food)
               WHERE f.name IN ['林区山野菜', '松子']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建关系：景点→附近美食
            session.run("""
               MATCH (a:Attraction {name: '日月峡国家森林公园'}), (f:Food {name: '林区山野菜'})
               CREATE (a)-[:NEAR_FOOD {distance: '附近可品尝新鲜山野菜'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '日月峡国家森林公园'}), (f:Food {name: '松子'})
               CREATE (a)-[:NEAR_FOOD {distance: '景区及周边可购买'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '桃山国际狩猎场'}), (f:Food)
               WHERE f.name IN ['林区山野菜', '松子']
               CREATE (a)-[:NEAR_FOOD {distance: '狩猎场及周边可找到'}]->(f)
           """)

            # 7. 创建关系：景点→附近住宿
            session.run("""
               MATCH (a:Attraction {name: '桃山国际狩猎场'}), (ac:Accommodation {name: '桃山宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '位于狩猎场内'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '日月峡国家森林公园'}), (ac:Accommodation {name: '铁力宇祥国际酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '建议住宿市区'}]->(ac)
           """)

            # 8. 创建关系：城市→交通
            session.run("""
               MATCH (c:City {name: '铁力'}), (t:Transportation)
               WHERE t.name IN ['铁力市区公交', '铁力客运站班车']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)

        print("铁力市旅游数据导入完成！")

    def import_tongjiang_data(self):
        """导入同江市旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (tongjiang:City {name: '同江', level: '县级市', description: '黑龙江省佳木斯市代管的县级市，位于松花江与黑龙江汇流处，是中国“六小”民族之一赫哲族的主要聚居地，被誉为“赫哲故里”、“口岸名城”'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (sanjiangkou:Attraction {name: '三江口生态旅游区', type: '自然景观', rating: 4.6, opening_hours: '全天开放'}),
               (jiejinkou:Attraction {name: '街津口赫哲族旅游度假区', type: '人文+自然景观', rating: 4.5, opening_hours: '8:30-17:00'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (shengshayu:Food {name: '赫哲族杀生鱼', type: '民族特色', price_range: '中', description: '用新鲜活鱼制成，口感爽脆，风味独特'}),
               (talaha2:Food {name: '塔拉哈', type: '民族特色', price_range: '中', description: '烤制的半生鱼片，带有炙烤香气'}),
               (xinyuandong:Accommodation {name: '同江新远东国际酒店', type: '商务酒店', price_range: '中', rating: 4.3}),
               (hezeminsu:Accommodation {name: '街津口赫哲族民宿', type: '民宿', price_range: '低', rating: 4.5}),
               (tongjiangbus:Transportation {name: '同江市区公交', type: '公交', route: '覆盖城区', price: '1-2元'}),
               (tongjiang2jiejin:Transportation {name: '同江至街津口班车', type: '旅游班车', route: '市区-赫哲族乡', price: '约10元'})
           """)

            # 4. 创建关系：景点→城市
            session.run("""
               MATCH (a:Attraction), (c:City {name: '同江'})
               WHERE a.name IN ['三江口生态旅游区', '街津口赫哲族旅游度假区']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建关系：城市→推荐美食
            session.run("""
               MATCH (c:City {name: '同江'}), (f:Food)
               WHERE f.name IN ['赫哲族杀生鱼', '塔拉哈']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建关系：景点→附近美食
            session.run("""
               MATCH (a:Attraction {name: '街津口赫哲族旅游度假区'}), (f:Food)
               WHERE f.name IN ['赫哲族杀生鱼', '塔拉哈']
               CREATE (a)-[:NEAR_FOOD {distance: '度假区内可品尝最正宗赫哲族美食'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '三江口生态旅游区'}), (f:Food)
               WHERE f.name IN ['赫哲族杀生鱼', '塔拉哈']
               CREATE (a)-[:NEAR_FOOD {distance: '市区及街津口可找到'}]->(f)
           """)

            # 7. 创建关系：景点→附近住宿
            session.run("""
               MATCH (a:Attraction {name: '街津口赫哲族旅游度假区'}), (ac:Accommodation {name: '街津口赫哲族民宿'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '位于度假区内'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '三江口生态旅游区'}), (ac:Accommodation {name: '同江新远东国际酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '市区住宿便利'}]->(ac)
           """)

            # 8. 创建关系：城市→交通
            session.run("""
               MATCH (c:City {name: '同江'}), (t:Transportation)
               WHERE t.name IN ['同江市区公交', '同江至街津口班车']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)

        print("同江市旅游数据导入完成！")

    def import_fujin_data(self):
        """导入富锦市旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (fujin:City {name: '富锦', level: '县级市', description: '黑龙江省佳木斯市代管的县级市，坐落于三江平原腹地，是“中国东北大米之乡”和“北大荒精准农业示范中心”，被誉为“黑土绿洲”'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (shidigongyuan:Attraction {name: '富锦国家湿地公园', type: '自然景观', rating: 4.7, opening_hours: '8:00-17:00'}),
               (daomidagongyuan:Attraction {name: '万亩水稻公园', type: '农业观光', rating: 4.4, opening_hours: '全天开放（夏秋最佳）'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (fujindami:Food {name: '富锦大米饭', type: '地方特产', price_range: '中', description: '颗粒饱满，饭香浓郁'}),
               (tieguodun:Food {name: '铁锅炖大鹅', type: '东北菜', price_range: '中', description: '肉质紧实，汤汁浓郁'}),
               (jindubinguan:Accommodation {name: '富锦金都宾馆', type: '商务酒店', price_range: '中', rating: 4.2}),
               (dongfangdasha:Accommodation {name: '富锦东方大厦', type: '商务酒店', price_range: '中', rating: 4.1}),
               (fujinbus:Transportation {name: '富锦市区公交', type: '公交', route: '覆盖城区', price: '1-2元'}),
               (fujinkeyun:Transportation {name: '富锦客运站班车', type: '大巴', route: '连通佳木斯、哈尔滨等地', price: '依里程而定'})
           """)

            # 4. 创建关系：景点→城市
            session.run("""
               MATCH (a:Attraction), (c:City {name: '富锦'})
               WHERE a.name IN ['富锦国家湿地公园', '万亩水稻公园']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建关系：城市→推荐美食
            session.run("""
               MATCH (c:City {name: '富锦'}), (f:Food)
               WHERE f.name IN ['富锦大米饭', '铁锅炖大鹅']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建关系：景点→附近美食
            session.run("""
               MATCH (a:Attraction {name: '万亩水稻公园'}), (f:Food {name: '富锦大米饭'})
               CREATE (a)-[:NEAR_FOOD {distance: '可体验和购买正宗富锦大米'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '万亩水稻公园'}), (f:Food {name: '铁锅炖大鹅'})
               CREATE (a)-[:NEAR_FOOD {distance: '周边餐馆可提供'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '富锦国家湿地公园'}), (f:Food)
               WHERE f.name IN ['富锦大米饭', '铁锅炖大鹅']
               CREATE (a)-[:NEAR_FOOD {distance: '需返回市区品尝'}]->(f)
           """)

            # 7. 创建关系：景点→附近住宿
            session.run("""
               MATCH (a:Attraction {name: '富锦国家湿地公园'}), (ac:Accommodation)
               WHERE ac.name IN ['富锦金都宾馆', '富锦东方大厦']
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '需返回市区'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '万亩水稻公园'}), (ac:Accommodation)
               WHERE ac.name IN ['富锦金都宾馆', '富锦东方大厦']
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '市区住宿便利'}]->(ac)
           """)

            # 8. 创建关系：城市→交通
            session.run("""
               MATCH (c:City {name: '富锦'}), (t:Transportation)
               WHERE t.name IN ['富锦市区公交', '富锦客运站班车']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)

        print("富锦市旅游数据导入完成！")

    def import_fuyuan_data(self):
        """导入抚远市旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (fuyuan:City {name: '抚远', level: '县级市', description: '黑龙江省佳木斯市代管的县级市，位于中国最东端，是每天最早将太阳迎进祖国的地方，被誉为“华夏东极”、“淡水鱼都”'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (heixiazi_fuyuan:Attraction {name: '黑瞎子岛', type: '自然+人文景观', rating: 4.6, opening_hours: '8:30-17:00'}),
               (dongjiguangchang:Attraction {name: '东极广场', type: '人文景观', rating: 4.7, opening_hours: '全天开放'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (quanyuyan:Food {name: '抚远全鱼宴', type: '地方特色', price_range: '中高', description: '汇聚黑龙江、乌苏里江各种珍稀江鱼，烹饪方式多样'}),
               (xunhuangyuzi:Food {name: '鲟鳇鱼子酱', type: '地方特产', price_range: '高', description: '世界顶级食材，口感醇厚'}),
               (fuyuandongfang:Accommodation {name: '抚远东方宾馆', type: '商务酒店', price_range: '中', rating: 4.3}),
               (heixiazidao:Accommodation {name: '黑瞎子岛露营地', type: '特色住宿', price_range: '中', rating: 4.5}),
               (fuyuanbus:Transportation {name: '抚远市区公交', type: '公交', route: '覆盖城区', price: '1-2元'}),
               (fuyuanairport:Transportation {name: '抚远机场大巴', type: '大巴', route: '机场-市区', price: '20元'})
           """)

            # 4. 创建关系：景点→城市
            session.run("""
               MATCH (a:Attraction), (c:City {name: '抚远'})
               WHERE a.name IN ['黑瞎子岛', '东极广场']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建关系：城市→推荐美食
            session.run("""
               MATCH (c:City {name: '抚远'}), (f:Food)
               WHERE f.name IN ['抚远全鱼宴', '鲟鳇鱼子酱']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建关系：景点→附近美食
            session.run("""
               MATCH (a:Attraction {name: '黑瞎子岛'}), (f:Food)
               WHERE f.name IN ['抚远全鱼宴', '鲟鳇鱼子酱']
               CREATE (a)-[:NEAR_FOOD {distance: '附近可品尝新鲜江鱼及相关制品'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '东极广场'}), (f:Food)
               WHERE f.name IN ['抚远全鱼宴', '鲟鳇鱼子酱']
               CREATE (a)-[:NEAR_FOOD {distance: '市区内餐馆可提供'}]->(f)
           """)

            # 7. 创建关系：景点→附近住宿
            session.run("""
               MATCH (a:Attraction {name: '东极广场'}), (ac:Accommodation {name: '抚远东方宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '约5km'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '黑瞎子岛'}), (ac:Accommodation {name: '黑瞎子岛露营地'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '位于岛附近'}]->(ac)
           """)

            # 8. 创建关系：城市→交通
            session.run("""
               MATCH (c:City {name: '抚远'}), (t:Transportation)
               WHERE t.name IN ['抚远市区公交', '抚远机场大巴']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)

        print("抚远市旅游数据导入完成！")

    def import_suifenhe_data(self):
        """导入绥芬河市旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (suifenhe:City {name: '绥芬河', level: '县级市', description: '黑龙江省牡丹江市代管的县级市，是中国重要的对俄陆路口岸，被誉为“中俄商贸之都”、“火车拉来的城市”，充满浓郁的俄式风情'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (guomen:Attraction {name: '绥芬河国门景区', type: '人文景观', rating: 4.5, opening_hours: '8:00-17:00'}),
               (dabailou:Attraction {name: '大白楼（中东铁路记忆馆）', type: '人文景观', rating: 4.4, opening_hours: '9:00-16:30'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (eshi烤肉:Food {name: '俄式烤肉', type: '异国风味', price_range: '中', description: '量大实惠，肉香浓郁'}),
               (gewasi:Food {name: '格瓦斯', type: '饮品', price_range: '低', description: '俄式传统发酵饮料，口感独特'}),
               (kaixiang:Accommodation {name: '绥芬河凯翔国际酒店', type: '商务酒店', price_range: '中', rating: 4.4}),
               (makesimu:Accommodation {name: '绥芬河马克西姆宾馆', type: '俄式特色酒店', price_range: '中', rating: 4.3}),
               (suifenhebus:Transportation {name: '绥芬河市内公交', type: '公交', route: '覆盖城区及口岸', price: '1-2元'}),
               (guojilieche:Transportation {name: '国际列车', type: '铁路', route: '绥芬河-格罗迭科沃（俄罗斯）'})
           """)

            # 4. 创建关系：景点→城市
            session.run("""
               MATCH (a:Attraction), (c:City {name: '绥芬河'})
               WHERE a.name IN ['绥芬河国门景区', '大白楼（中东铁路记忆馆）']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建关系：城市→推荐美食
            session.run("""
               MATCH (c:City {name: '绥芬河'}), (f:Food)
               WHERE f.name IN ['俄式烤肉', '格瓦斯']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建关系：景点→附近美食
            session.run("""
               MATCH (a:Attraction {name: '绥芬河国门景区'}), (f:Food)
               WHERE f.name IN ['俄式烤肉', '格瓦斯']
               CREATE (a)-[:NEAR_FOOD {distance: '附近可体验俄式餐厅'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '大白楼（中东铁路记忆馆）'}), (f:Food)
               WHERE f.name IN ['俄式烤肉', '格瓦斯']
               CREATE (a)-[:NEAR_FOOD {distance: '市区内俄式餐馆密集'}]->(f)
           """)

            # 7. 创建关系：景点→附近住宿
            session.run("""
               MATCH (a:Attraction), (ac:Accommodation)
               WHERE a.name IN ['绥芬河国门景区', '大白楼（中东铁路记忆馆）']
                 AND ac.name IN ['绥芬河凯翔国际酒店', '绥芬河马克西姆宾馆']
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '市区内住宿选择多样'}]->(ac)
           """)

            # 8. 创建关系：城市→交通
            session.run("""
               MATCH (c:City {name: '绥芬河'}), (t:Transportation)
               WHERE t.name IN ['绥芬河市内公交', '国际列车']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)

        print("绥芬河市旅游数据导入完成！")

    def import_hailin_data(self):
        """导入海林市旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (hailin:City {name: '海林', level: '县级市', description: '黑龙江省牡丹江市代管的县级市，位于张广才岭东麓，是经典小说《林海雪原》的故事发生地，被誉为“林海雪原”、“中国虎乡”'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (xuexiang_hailin:Attraction {name: '中国雪乡（双峰林场）', type: '自然+人文景观', rating: 4.5, opening_hours: '全天开放'}),
               (weihushan:Attraction {name: '威虎山城影视基地', type: '人文景观', rating: 4.3, opening_hours: '8:30-17:00'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (linqubadawan:Food {name: '林区八大碗', type: '地方特色', price_range: '中', description: '源自林区传统宴客菜，用料实在，风味淳朴'}),
               (yeshenghoutougu:Food {name: '野生猴头菇', type: '山珍', price_range: '中高', description: '名贵食材，炖汤味道极其鲜美'}),
               (xuexiangminsu:Accommodation {name: '雪乡民宿', type: '特色民宿', price_range: '中高（旺季浮动大）', rating: 4.4}),
               (hailinbinguan:Accommodation {name: '海林市宾馆', type: '商务酒店', price_range: '中', rating: 4.2}),
               (hailinbus:Transportation {name: '海林市区公交', type: '公交', route: '覆盖城区', price: '1-2元'}),
               (lvyoutongche:Transportation {name: '旅游直通车', type: '大巴', route: '牡丹江/海林-雪乡', price: '约40元'})
           """)

            # 4. 创建关系：景点→城市
            session.run("""
               MATCH (a:Attraction), (c:City {name: '海林'})
               WHERE a.name IN ['中国雪乡（双峰林场）', '威虎山城影视基地']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建关系：城市→推荐美食
            session.run("""
               MATCH (c:City {name: '海林'}), (f:Food)
               WHERE f.name IN ['林区八大碗', '野生猴头菇']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建关系：景点→附近美食
            session.run("""
               MATCH (a:Attraction {name: '中国雪乡（双峰林场）'}), (f:Food)
               WHERE f.name IN ['林区八大碗', '野生猴头菇']
               CREATE (a)-[:NEAR_FOOD {distance: '景区内可品尝地道林区菜'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '威虎山城影视基地'}), (f:Food)
               WHERE f.name IN ['林区八大碗', '野生猴头菇']
               CREATE (a)-[:NEAR_FOOD {distance: '市区及周边可找到'}]->(f)
           """)

            # 7. 创建关系：景点→附近住宿
            session.run("""
               MATCH (a:Attraction {name: '威虎山城影视基地'}), (ac:Accommodation {name: '海林市宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '需返回海林市区或前往长汀镇'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '中国雪乡（双峰林场）'}), (ac:Accommodation {name: '雪乡民宿'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '位于景区内'}]->(ac)
           """)

            # 8. 创建关系：城市→交通
            session.run("""
               MATCH (c:City {name: '海林'}), (t:Transportation)
               WHERE t.name IN ['海林市区公交', '旅游直通车']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)

        print("海林市旅游数据导入完成！")

    def import_ningan_data(self):
        """导入宁安市旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (ningan:City {name: '宁安', level: '县级市', description: '黑龙江省牡丹江市代管的县级市，历史悠久，是满族先祖肃慎人的发祥地之一，拥有世界级地质景观镜泊湖，被誉为“塞北江南”'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (jingpohu_ningan:Attraction {name: '镜泊湖风景区', type: '自然景观', rating: 4.8, opening_hours: '全天开放'}),
               (bohaiguo:Attraction {name: '渤海国上京龙泉府遗址', type: '人文景观', rating: 4.4, opening_hours: '9:00-17:00'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (hongweiyu:Food {name: '镜泊湖红尾鱼', type: '地方特色', price_range: '中', description: '生长于镜泊湖，肉质紧实，味道鲜美'}),
               (huoshanyanmida:Food {name: '宁安火山岩大米', type: '地方特产', price_range: '中', description: '在火山熔岩台地上种植，米质上乘'}),
               (jingpohubg:Accommodation {name: '镜泊湖宾馆', type: '度假酒店', price_range: '中高', rating: 4.5}),
               (xinjiegj:Accommodation {name: '宁安鑫街国际酒店', type: '商务酒店', price_range: '中', rating: 4.3}),
               (ninganbus:Transportation {name: '宁安市区公交', type: '公交', route: '覆盖城区', price: '1-2元'}),
               (ningan2jingpo:Transportation {name: '宁安至镜泊湖班车', type: '旅游班车', route: '市区-镜泊湖景区', price: '约15元'})
           """)

            # 4. 创建关系：景点→城市
            session.run("""
               MATCH (a:Attraction), (c:City {name: '宁安'})
               WHERE a.name IN ['镜泊湖风景区', '渤海国上京龙泉府遗址']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建关系：城市→推荐美食
            session.run("""
               MATCH (c:City {name: '宁安'}), (f:Food)
               WHERE f.name IN ['镜泊湖红尾鱼', '宁安火山岩大米']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建关系：景点→附近美食
            session.run("""
               MATCH (a:Attraction {name: '镜泊湖风景区'}), (f:Food {name: '镜泊湖红尾鱼'})
               CREATE (a)-[:NEAR_FOOD {distance: '景区周边鱼馆可提供'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '镜泊湖风景区'}), (f:Food {name: '宁安火山岩大米'})
               CREATE (a)-[:NEAR_FOOD {distance: '景区及市区可购买'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '渤海国上京龙泉府遗址'}), (f:Food)
               WHERE f.name IN ['镜泊湖红尾鱼', '宁安火山岩大米']
               CREATE (a)-[:NEAR_FOOD {distance: '市区内可找到'}]->(f)
           """)

            # 7. 创建关系：景点→附近住宿
            session.run("""
               MATCH (a:Attraction {name: '镜泊湖风景区'}), (ac:Accommodation {name: '镜泊湖宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '位于景区内'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '渤海国上京龙泉府遗址'}), (ac:Accommodation {name: '宁安鑫街国际酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '市区住宿便利'}]->(ac)
           """)

            # 8. 创建关系：城市→交通
            session.run("""
               MATCH (c:City {name: '宁安'}), (t:Transportation)
               WHERE t.name IN ['宁安市区公交', '宁安至镜泊湖班车']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)

        print("宁安市旅游数据导入完成！")

    def import_muling_data(self):
        """导入穆棱市旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (muling:City {name: '穆棱', level: '县级市', description: '黑龙江省牡丹江市代管的县级市，名源于“穆棱河”，是“中国大豆之乡”和“东北红豆杉之乡”，一座位于张广才岭下的生态之城'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (liufenghu:Attraction {name: '六峰湖国家森林公园', type: '自然景观', rating: 4.5, opening_hours: '8:00-17:00'}),
               (hongdoushan:Attraction {name: '红豆杉广场', type: '人文+自然景观', rating: 4.2, opening_hours: '全天开放'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (dadouyan:Food {name: '穆棱大豆宴', type: '地方特色', price_range: '中低', description: '以优质非转基因大豆为原料，制作豆腐、豆浆等各式菜肴'}),
               (linquxiaochao:Food {name: '林区小炒', type: '地方特色', price_range: '中低', description: '选用山野菜、菌菇等本地食材，清新爽口'}),
               (wanshida:Accommodation {name: '穆棱万事达酒店', type: '商务酒店', price_range: '中', rating: 4.3}),
               (jiedaizhongxin:Accommodation {name: '穆棱接待中心', type: '商务酒店', price_range: '中低', rating: 4.1}),
               (mulingbus:Transportation {name: '穆棱市区公交', type: '公交', route: '覆盖城区', price: '1-2元'}),
               (mulingkeyun:Transportation {name: '穆棱客运站班车', type: '大巴', route: '连通牡丹江、绥芬河等地', price: '依里程而定'})
           """)

            # 4. 创建关系：景点→城市
            session.run("""
               MATCH (a:Attraction), (c:City {name: '穆棱'})
               WHERE a.name IN ['六峰湖国家森林公园', '红豆杉广场']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建关系：城市→推荐美食
            session.run("""
               MATCH (c:City {name: '穆棱'}), (f:Food)
               WHERE f.name IN ['穆棱大豆宴', '林区小炒']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建关系：景点→附近美食
            session.run("""
               MATCH (a:Attraction), (f:Food)
               WHERE a.name IN ['六峰湖国家森林公园', '红豆杉广场']
                 AND f.name IN ['穆棱大豆宴', '林区小炒']
               CREATE (a)-[:NEAR_FOOD {distance: '市区内餐馆可品尝到'}]->(f)
           """)

            # 7. 创建关系：景点→附近住宿
            session.run("""
               MATCH (a:Attraction {name: '六峰湖国家森林公园'}), (ac:Accommodation)
               WHERE ac.name IN ['穆棱万事达酒店', '穆棱接待中心']
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '需返回市区'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '红豆杉广场'}), (ac:Accommodation)
               WHERE ac.name IN ['穆棱万事达酒店', '穆棱接待中心']
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '市区内住宿便利'}]->(ac)
           """)

            # 8. 创建关系：城市→交通
            session.run("""
               MATCH (c:City {name: '穆棱'}), (t:Transportation)
               WHERE t.name IN ['穆棱市区公交', '穆棱客运站班车']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)

        print("穆棱市旅游数据导入完成！")

    def import_dongning_data(self):
        """导入东宁市旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (dongning:City {name: '东宁', level: '县级市', description: '黑龙江省牡丹江市代管的县级市，位于黑龙江省最南端，是重要的对俄口岸城市，也是“中国黑木耳第一县”，被誉为“塞北小江南”'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (yaosaiqun:Attraction {name: '东宁要塞群遗址', type: '人文景观/二战遗址', rating: 4.5, opening_hours: '8:30-16:30'}),
               (dongting:Attraction {name: '洞庭风景区', type: '自然景观', rating: 4.4, opening_hours: '8:00-17:00'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (heimuer:Food {name: '东宁黑木耳', type: '地方特产', price_range: '中低', description: '肉厚无根，口感爽脆，可凉拌、热炒'}),
               (eshichang:Food {name: '俄式风味肠', type: '异国风味', price_range: '中', description: '受俄罗斯饮食文化影响，种类繁多，风味独特'}),
               (jixiang:Accommodation {name: '东宁吉祥大酒店', type: '商务酒店', price_range: '中', rating: 4.3}),
               (kouanbinguan:Accommodation {name: '东宁口岸宾馆', type: '商务酒店', price_range: '中', rating: 4.2}),
               (dongningbus:Transportation {name: '东宁市区公交', type: '公交', route: '覆盖城区', price: '1-2元'}),
               (dongningkeyun:Transportation {name: '东宁客运站班车', type: '大巴', route: '连通绥芬河、牡丹江等地', price: '依里程而定'})
           """)

            # 4. 创建关系：景点→城市
            session.run("""
               MATCH (a:Attraction), (c:City {name: '东宁'})
               WHERE a.name IN ['东宁要塞群遗址', '洞庭风景区']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建关系：城市→推荐美食
            session.run("""
               MATCH (c:City {name: '东宁'}), (f:Food)
               WHERE f.name IN ['东宁黑木耳', '俄式风味肠']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建关系：景点→附近美食
            session.run("""
               MATCH (a:Attraction), (f:Food {name: '东宁黑木耳'})
               WHERE a.name IN ['东宁要塞群遗址', '洞庭风景区']
               CREATE (a)-[:NEAR_FOOD {distance: '市区各大市场及餐馆可提供'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction), (f:Food {name: '俄式风味肠'})
               WHERE a.name IN ['东宁要塞群遗址', '洞庭风景区']
               CREATE (a)-[:NEAR_FOOD {distance: '市区内可找到俄式餐馆'}]->(f)
           """)

            # 7. 创建关系：景点→附近住宿
            session.run("""
               MATCH (a:Attraction {name: '东宁要塞群遗址'}), (ac:Accommodation)
               WHERE ac.name IN ['东宁吉祥大酒店', '东宁口岸宾馆']
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '需返回市区'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '洞庭风景区'}), (ac:Accommodation)
               WHERE ac.name IN ['东宁吉祥大酒店', '东宁口岸宾馆']
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '建议返回市区住宿'}]->(ac)
           """)

            # 8. 创建关系：城市→交通
            session.run("""
               MATCH (c:City {name: '东宁'}), (t:Transportation)
               WHERE t.name IN ['东宁市区公交', '东宁客运站班车']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)

        print("东宁市旅游数据导入完成！")

    def import_bei_an_data(self):
        """导入北安市旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (bei_an:City {name: '北安', level: '县级市', description: '黑龙江省黑河市代管的县级市，位于松嫩平原边缘，是黑龙江省北部区域性中心城市，历史上曾为黑龙江省省会，被誉为“北国枪城”、“塞北延安”'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (bei_an_museum:Attraction {name: '北安博物馆', type: '人文景观', rating: 4.4, opening_hours: '9:00-16:00 (周一闭馆)'}),
               (qinghua_museum:Attraction {name: '庆华军工遗址博物馆', type: '人文景观/工业旅游', rating: 4.5, opening_hours: '8:30-16:30'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (bei_an_kao_leng_mian:Food {name: '北安烤冷面', type: '地方小吃', price_range: '低', description: '酱料独特，是当地流行的街头美食'}),
               (dongbei_jiang_gu_tou:Food {name: '东北酱骨头', type: '东北菜', price_range: '中', description: '酱香浓郁，肉质软烂入味'}),
               (jin_jie_hotel:Accommodation {name: '北安金街国际酒店', type: '商务酒店', price_range: '中', rating: 4.3}),
               (xiang_he_hotel:Accommodation {name: '北安祥和宾馆', type: '经济型酒店', price_range: '低', rating: 4.1}),
               (bei_an_bus:Transportation {name: '北安市区公交', type: '公交', route: '覆盖城区', price: '1-2元'}),
               (bei_an_bus_station:Transportation {name: '北安客运站班车', type: '大巴', route: '连通哈尔滨、黑河、五大连池等地', price: '依里程而定'})
           """)

            # 4. 创建关系：景点→城市
            session.run("""
               MATCH (a:Attraction), (c:City {name: '北安'})
               WHERE a.name IN ['北安博物馆', '庆华军工遗址博物馆']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建关系：城市→推荐美食
            session.run("""
               MATCH (c:City {name: '北安'}), (f:Food)
               WHERE f.name IN ['北安烤冷面', '东北酱骨头']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建关系：景点→附近美食
            session.run("""
               MATCH (a:Attraction), (f:Food)
               WHERE a.name IN ['北安博物馆', '庆华军工遗址博物馆']
                 AND f.name IN ['北安烤冷面', '东北酱骨头']
               CREATE (a)-[:NEAR_FOOD {distance: '市区内可方便找到'}]->(f)
           """)

            # 7. 创建关系：景点→附近住宿
            session.run("""
               MATCH (a:Attraction), (ac:Accommodation {name: '北安金街国际酒店'})
               WHERE a.name IN ['北安博物馆', '庆华军工遗址博物馆']
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '位于市中心，交通便利'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction), (ac:Accommodation {name: '北安祥和宾馆'})
               WHERE a.name IN ['北安博物馆', '庆华军工遗址博物馆']
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '市区内经济型选择'}]->(ac)
           """)

            # 8. 创建关系：城市→交通
            session.run("""
               MATCH (c:City {name: '北安'}), (t:Transportation)
               WHERE t.name IN ['北安市区公交', '北安客运站班车']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)

        print("北安市旅游数据导入完成！")

    def import_wu_da_lian_chi_data(self):
        """导入五大连池市旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (wu_da_lian_chi:City {name: '五大连池', level: '县级市', description: '黑龙江省黑河市代管的县级市，以世界著名的火山群和矿泉资源命名，被誉为“天然的火山博物馆”和“世界三大冷泉之一”，是著名的康疗养生胜地'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (wu_da_lian_chi_scenic:Attraction {name: '五大连池风景区', type: '自然景观', rating: 4.8, opening_hours: '全天开放（各景点单独售票，时间不一）'}),
               (yao_quan_shan:Attraction {name: '药泉山', type: '自然景观', rating: 4.6, opening_hours: '8:00-17:00'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (kuang_quan_dou_fu:Food {name: '矿泉豆腐', type: '地方特色', price_range: '中低', description: '用天然矿泉水制作，豆香浓郁，口感嫩滑'}),
               (kuang_quan_yu:Food {name: '矿泉鱼', type: '地方特色', price_range: '中', description: '生长在火山堰塞湖中，无土腥味，味道鲜美'}),
               (wan_hao_hotel:Accommodation {name: '五大连池万豪名苑商务酒店', type: '商务酒店', price_range: '中', rating: 4.4}),
               (gong_ren_liao_yang_yuan:Accommodation {name: '工人疗养院', type: '疗养酒店', price_range: '中', rating: 4.5}),
               (sightseeing_bus:Transportation {name: '五大连池旅游观光车', type: '旅游巴士', route: '连接景区内各主要景点', price: '含在景区联票内'}),
               (wu_da_lian_chi_bus_station:Transportation {name: '五大连池客运站班车', type: '大巴', route: '主要通往北安、哈尔滨等地', price: '依里程而定'})
           """)

            # 4. 创建关系：景点→城市
            session.run("""
               MATCH (a:Attraction), (c:City {name: '五大连池'})
               WHERE a.name IN ['五大连池风景区', '药泉山']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建关系：城市→推荐美食
            session.run("""
               MATCH (c:City {name: '五大连池'}), (f:Food)
               WHERE f.name IN ['矿泉豆腐', '矿泉鱼']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建关系：景点→附近美食
            session.run("""
               MATCH (a:Attraction {name: '五大连池风景区'}), (f:Food)
               WHERE f.name IN ['矿泉豆腐', '矿泉鱼']
               CREATE (a)-[:NEAR_FOOD {distance: '风景区内餐馆基本都提供'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '药泉山'}), (f:Food)
               WHERE f.name IN ['矿泉豆腐', '矿泉鱼']
               CREATE (a)-[:NEAR_FOOD {distance: '景区周边餐馆可提供'}]->(f)
           """)

            # 7. 创建关系：景点→附近住宿
            session.run("""
               MATCH (a:Attraction {name: '五大连池风景区'}), (ac:Accommodation {name: '工人疗养院'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '位于景区核心地带'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '药泉山'}), (ac:Accommodation)
               WHERE ac.name IN ['五大连池万豪名苑商务酒店', '工人疗养院']
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '景区及市区均有住宿选择'}]->(ac)
           """)

            # 8. 创建关系：城市→交通
            session.run("""
               MATCH (c:City {name: '五大连池'}), (t:Transportation)
               WHERE t.name IN ['五大连池旅游观光车', '五大连池客运站班车']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)

        print("五大连池市旅游数据导入完成！")

    def import_nenjiang_data(self):
        """导入嫩江市旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (nenjiang:City {name: '嫩江', level: '县级市', description: '黑龙江省黑河市代管的县级市，因嫩江得名，地处松嫩平原连接大、小兴安岭的过渡地带，是“中国大豆之乡”，被誉为“北国粮仓”'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (jiangpan:Attraction {name: '江畔公园', type: '自然+人文景观', rating: 4.4, opening_hours: '全天开放'}),
               (moergen:Attraction {name: '墨尔根古道驿站博物馆', type: '人文景观', rating: 4.3, opening_hours: '9:00-16:30'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (quandouyan:Food {name: '全豆宴', type: '地方特色', price_range: '中', description: '以非转基因大豆为原料，开发出丰富多样的豆制品菜肴'}),
               (nenjiangyu:Food {name: '江鱼', type: '地方特色', price_range: '中', description: '取自嫩江，肉质鲜美，做法多样'}),
               (shangmaogj:Accommodation {name: '嫩江商贸国际酒店', type: '商务酒店', price_range: '中', rating: 4.3}),
               (nenjiangbg:Accommodation {name: '嫩江宾馆', type: '商务酒店', price_range: '中', rating: 4.2}),
               (nenjiangbus:Transportation {name: '嫩江市区公交', type: '公交', route: '覆盖城区', price: '1-2元'}),
               (nenjiangkeyun:Transportation {name: '嫩江客运站班车', type: '大巴', route: '连通黑河、齐齐哈尔、哈尔滨等地', price: '依里程而定'})
           """)

            # 4. 创建关系：景点→城市
            session.run("""
               MATCH (a:Attraction), (c:City {name: '嫩江'})
               WHERE a.name IN ['江畔公园', '墨尔根古道驿站博物馆']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建关系：城市→推荐美食
            session.run("""
               MATCH (c:City {name: '嫩江'}), (f:Food)
               WHERE f.name IN ['全豆宴', '江鱼']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建关系：景点→附近美食
            session.run("""
               MATCH (a:Attraction {name: '江畔公园'}), (f:Food {name: '江鱼'})
               CREATE (a)-[:NEAR_FOOD {distance: '附近可品尝到新鲜江鱼'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '墨尔根古道驿站博物馆'}), (f:Food {name: '全豆宴'})
               CREATE (a)-[:NEAR_FOOD {distance: '市区内餐馆可体验'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction), (f:Food)
               WHERE (a.name = '江畔公园' AND f.name = '全豆宴') OR (a.name = '墨尔根古道驿站博物馆' AND f.name = '江鱼')
               CREATE (a)-[:NEAR_FOOD {distance: '市区内可找到'}]->(f)
           """)

            # 7. 创建关系：景点→附近住宿
            session.run("""
               MATCH (a:Attraction), (ac:Accommodation)
               WHERE a.name IN ['江畔公园', '墨尔根古道驿站博物馆']
                 AND ac.name IN ['嫩江商贸国际酒店', '嫩江宾馆']
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '市区内住宿便利'}]->(ac)
           """)

            # 8. 创建关系：城市→交通
            session.run("""
               MATCH (c:City {name: '嫩江'}), (t:Transportation)
               WHERE t.name IN ['嫩江市区公交', '嫩江客运站班车']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)

        print("嫩江市旅游数据导入完成！")

    def import_andan_data(self):
        """导入安达市旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (andan:City {name: '安达', level: '县级市', description: '黑龙江省绥化市代管的县级市，名字源自满语“朋友”，是中国著名的“奶牛之乡”和“石化之城”，享有“牛城”的美誉'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (donghu:Attraction {name: '东湖湿地', type: '自然景观', rating: 4.3, opening_hours: '全天开放'}),
               (niuwenhua:Attraction {name: '安达牛文化博物馆', type: '人文景观', rating: 4.4, opening_hours: '9:00-16:00'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (naizhipin:Food {name: '安达奶制品', type: '地方特产', price_range: '低', description: '鲜奶、酸奶、奶酪等，奶源纯正，品质上乘'}),
               (tanhuo:Food {name: '炭火烤肉', type: '地方特色', price_range: '中', description: '选用优质牛羊肉，风味独特'}),
               (longfu:Accommodation {name: '安达龙府世家中州国际酒店', type: '商务酒店', price_range: '中', rating: 4.3}),
               (baixiang:Accommodation {name: '安达百祥宾馆', type: '经济型酒店', price_range: '低', rating: 4.1}),
               (andanbus:Transportation {name: '安达市区公交', type: '公交', route: '覆盖城区', price: '1-2元'}),
               (andakeyun:Transportation {name: '安达客运站班车', type: '大巴', route: '连通哈尔滨、大庆、绥化等地', price: '依里程而定'})
           """)

            # 4. 创建关系：景点→城市
            session.run("""
               MATCH (a:Attraction), (c:City {name: '安达'})
               WHERE a.name IN ['东湖湿地', '安达牛文化博物馆']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建关系：城市→推荐美食
            session.run("""
               MATCH (c:City {name: '安达'}), (f:Food)
               WHERE f.name IN ['安达奶制品', '炭火烤肉']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建关系：景点→附近美食
            session.run("""
               MATCH (a:Attraction {name: '安达牛文化博物馆'}), (f:Food {name: '安达奶制品'})
               CREATE (a)-[:NEAR_FOOD {distance: '附近可购买到正宗奶制品'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '东湖湿地'}), (f:Food {name: '炭火烤肉'})
               CREATE (a)-[:NEAR_FOOD {distance: '返回市区可体验'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction), (f:Food)
               WHERE (a.name = '安达牛文化博物馆' AND f.name = '炭火烤肉') OR (a.name = '东湖湿地' AND f.name = '安达奶制品')
               CREATE (a)-[:NEAR_FOOD {distance: '市区内可找到'}]->(f)
           """)

            # 7. 创建关系：景点→附近住宿
            session.run("""
               MATCH (a:Attraction), (ac:Accommodation)
               WHERE a.name IN ['东湖湿地', '安达牛文化博物馆']
                 AND ac.name IN ['安达龙府世家中州国际酒店', '安达百祥宾馆']
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '市区内住宿选择多样'}]->(ac)
           """)

            # 8. 创建关系：城市→交通
            session.run("""
               MATCH (c:City {name: '安达'}), (t:Transportation)
               WHERE t.name IN ['安达市区公交', '安达客运站班车']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)

        print("安达市旅游数据导入完成！")

    def import_zhaodong_data(self):
        """导入肇东市旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (zhaodong:City {name: '肇东', level: '县级市', description: '黑龙江省绥化市代管的县级市，位于松嫩平原腹地，哈尔滨大都市圈内，是重要的商品粮和畜牧业基地，素有“塞北江南”之称'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (zhaodong_shengtaiyuan:Attraction {name: '肇东生态园', type: '自然+人文景观', rating: 4.2, opening_hours: '全天开放'}),
               (balicheng:Attraction {name: '八里城遗址', type: '人文景观', rating: 4.1, opening_hours: '8:30-16:30'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (zhaodong_kaobing:Food {name: '肇东烤饼', type: '地方小吃', price_range: '低', description: '小饼烤制，刷上酱料，香酥可口，风味独特'}),
               (shazhucai:Food {name: '杀猪菜', type: '东北菜', price_range: '中低', description: '酸菜、血肠与猪肉的经典组合，乡土味浓'}),
               (huaguan_hotel:Accommodation {name: '肇东华冠大酒店', type: '商务酒店', price_range: '中', rating: 4.3}),
               (zhaodong_binguan:Accommodation {name: '肇东宾馆', type: '商务酒店', price_range: '中低', rating: 4.1}),
               (zhaodong_bus:Transportation {name: '肇东市区公交', type: '公交', route: '覆盖城区', price: '1-2元'}),
               (zhaodong_train_bus:Transportation {name: '肇东客运站班车/火车', type: '铁路/公路', route: '频繁往返哈尔滨', price: '10-30元'})
           """)

            # 4. 创建关系：景点→城市
            session.run("""
               MATCH (a:Attraction), (c:City {name: '肇东'})
               WHERE a.name IN ['肇东生态园', '八里城遗址']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建关系：城市→推荐美食
            session.run("""
               MATCH (c:City {name: '肇东'}), (f:Food)
               WHERE f.name IN ['肇东烤饼', '杀猪菜']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建关系：景点→附近美食
            session.run("""
               MATCH (a:Attraction), (f:Food {name: '肇东烤饼'})
               WHERE a.name IN ['肇东生态园', '八里城遗址']
               CREATE (a)-[:NEAR_FOOD {distance: '市区夜市及街边摊可品尝'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction), (f:Food {name: '杀猪菜'})
               WHERE a.name IN ['肇东生态园', '八里城遗址']
               CREATE (a)-[:NEAR_FOOD {distance: '市区东北菜馆可提供'}]->(f)
           """)

            # 7. 创建关系：景点→附近住宿
            session.run("""
               MATCH (a:Attraction {name: '肇东生态园'}), (ac:Accommodation {name: '肇东华冠大酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '约3km'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction), (ac:Accommodation)
               WHERE (a.name = '八里城遗址' AND ac.name IN ['肇东华冠大酒店', '肇东宾馆'])
                  OR (a.name = '肇东生态园' AND ac.name = '肇东宾馆')
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '市区内住宿便利'}]->(ac)
           """)

            # 8. 创建关系：城市→交通
            session.run("""
               MATCH (c:City {name: '肇东'}), (t:Transportation)
               WHERE t.name IN ['肇东市区公交', '肇东客运站班车/火车']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)

        print("肇东市旅游数据导入完成！")

    def import_hailun_data(self):
        """导入海伦市旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (hailun:City {name: '海伦', level: '县级市', description: '黑龙江省绥化市代管的县级市，位于小兴安岭脚下，是“中国优质大豆之乡”和“中国黑木耳之乡”，以富硒农产品闻名，被誉为“黑土硒都”'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (dadou_industry:Attraction {name: '海伦大豆产业园', type: '农业观光', rating: 4.3, opening_hours: '8:30-16:30'}),
               (dongfanghong:Attraction {name: '东方红水库', type: '自然景观', rating: 4.2, opening_hours: '全天开放'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (fuxi_dadouyan:Food {name: '富硒大豆宴', type: '地方特色', price_range: '中低', description: '利用富硒大豆开发的各种健康美食'}),
               (heimuer_cishen:Food {name: '黑木耳刺身', type: '地方特色', price_range: '中', description: '优质黑木耳鲜拌，口感爽脆，健康营养'}),
               (hailun_spring:Accommodation {name: '海伦春天酒店', type: '商务酒店', price_range: '中', rating: 4.2}),
               (hailun_binguan:Accommodation {name: '海伦宾馆', type: '商务酒店', price_range: '中低', rating: 4.0}),
               (hailun_bus:Transportation {name: '海伦市区公交', type: '公交', route: '覆盖城区', price: '1-2元'}),
               (hailun_keyun:Transportation {name: '海伦客运站班车', type: '大巴', route: '连通绥化、哈尔滨等地', price: '依里程而定'})
           """)

            # 4. 创建关系：景点→城市
            session.run("""
               MATCH (a:Attraction), (c:City {name: '海伦'})
               WHERE a.name IN ['海伦大豆产业园', '东方红水库']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建关系：城市→推荐美食
            session.run("""
               MATCH (c:City {name: '海伦'}), (f:Food)
               WHERE f.name IN ['富硒大豆宴', '黑木耳刺身']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建关系：景点→附近美食
            session.run("""
               MATCH (a:Attraction {name: '海伦大豆产业园'}), (f:Food {name: '富硒大豆宴'})
               CREATE (a)-[:NEAR_FOOD {distance: '可了解和购买富硒豆制品'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '东方红水库'}), (f:Food)
               WHERE f.name IN ['富硒大豆宴', '黑木耳刺身']
               CREATE (a)-[:NEAR_FOOD {distance: '需返回市区品尝'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '海伦大豆产业园'}), (f:Food {name: '黑木耳刺身'})
               CREATE (a)-[:NEAR_FOOD {distance: '市区内可找到'}]->(f)
           """)

            # 7. 创建关系：景点→附近住宿
            session.run("""
               MATCH (a:Attraction {name: '东方红水库'}), (ac:Accommodation)
               WHERE ac.name IN ['海伦春天酒店', '海伦宾馆']
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '需返回市区'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '海伦大豆产业园'}), (ac:Accommodation)
               WHERE ac.name IN ['海伦春天酒店', '海伦宾馆']
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '市区内住宿便利'}]->(ac)
           """)

            # 8. 创建关系：城市→交通
            session.run("""
               MATCH (c:City {name: '海伦'}), (t:Transportation)
               WHERE t.name IN ['海伦市区公交', '海伦客运站班车']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)

        print("海伦市旅游数据导入完成！")

    def import_mohe_data(self):
        """导入漠河市旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (mohe:City {name: '漠河', level: '县级市', description: '黑龙江省大兴安岭地区代管的县级市，位于中国版图的最北端，是中国纬度最高、气温最低的城市，被誉为“神州北极”，是观测北极光的最佳地点之一'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (beijicun:Attraction {name: '北极村', type: '自然+人文景观', rating: 4.7, opening_hours: '全天开放'}),
               (beihongcun:Attraction {name: '北红村', type: '自然+人文景观', rating: 4.6, opening_hours: '全天开放'}),
               (zhongguozuibeidian:Attraction {name: '中国最北点', type: '人文景观', rating: 4.7, opening_hours: '全天开放'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (lengshuiyuyan:Food {name: '冷水鱼宴', type: '地方特色', price_range: '中', description: '黑龙江的江鱼，肉质紧实，味道鲜美'}),
               (lanmei:Food {name: '蓝莓制品', type: '地方特产', price_range: '中低', description: '野生蓝莓制成的果汁、果酱等，纯天然'}),
               (beijicun_nongjiayuan:Accommodation {name: '北极村农家院', type: '特色民宿', price_range: '中', rating: 4.5}),
               (mohe_jinma:Accommodation {name: '漠河金马饭店', type: '商务酒店', price_range: '中', rating: 4.3}),
               (mohe_baoche:Transportation {name: '漠河旅游包车', type: '汽车', route: '连接市内各景点', price: '依行程而定'}),
               (mohe_keyun:Transportation {name: '漠河客运站班车', type: '大巴', route: '市区-北极村等', price: '约25元'})
           """)

            # 4. 创建关系：景点→城市
            session.run("""
               MATCH (a:Attraction), (c:City {name: '漠河'})
               WHERE a.name IN ['北极村', '北红村', '中国最北点']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建关系：城市→推荐美食
            session.run("""
               MATCH (c:City {name: '漠河'}), (f:Food)
               WHERE f.name IN ['冷水鱼宴', '蓝莓制品']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建关系：景点→附近美食
            session.run("""
               MATCH (a:Attraction {name: '北极村'}), (f:Food {name: '冷水鱼宴'})
               CREATE (a)-[:NEAR_FOOD {distance: '村内可品尝地道黑龙江冷水鱼'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction), (f:Food {name: '蓝莓制品'})
               WHERE a.name IN ['北极村', '北红村', '中国最北点']
               CREATE (a)-[:NEAR_FOOD {distance: '景区及市区可购买'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction)
               WHERE a.name IN ['北红村', '中国最北点']
               MATCH (f:Food {name: '冷水鱼宴'})
               CREATE (a)-[:NEAR_FOOD {distance: '附近餐馆可提供江鱼'}]->(f)
           """)

            # 7. 创建关系：景点→附近住宿
            session.run("""
               MATCH (a:Attraction {name: '北极村'}), (ac:Accommodation {name: '北极村农家院'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '位于村内'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction), (ac:Accommodation {name: '漠河金马饭店'})
               WHERE a.name IN ['北极村', '北红村', '中国最北点']
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '建议返回市区住宿'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction)
               WHERE a.name IN ['北红村', '中国最北点']
               MATCH (ac:Accommodation {name: '北极村农家院'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '可选择北极村住宿'}]->(ac)
           """)

            # 8. 创建关系：城市→交通
            session.run("""
               MATCH (c:City {name: '漠河'}), (t:Transportation)
               WHERE t.name IN ['漠河旅游包车', '漠河客运站班车']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)

        print("漠河市旅游数据导入完成！")

    def import_nanjing_data(self):
        """导入南京市旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (nanjing:City {name: '南京', level: '新一线城市', description: '江苏省省会，中国东部地区重要的中心城市，国家历史文化名城，被誉为“六朝古都”、“十朝都会”，兼具深厚历史底蕴与现代都市活力'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (zhongshanling:Attraction {name: '中山陵', type: '人文景观', rating: 4.8, opening_hours: '周二-周日 8:30-17:00'}),
               (fuzi庙:Attraction {name: '夫子庙-秦淮风光带', type: '人文景观', rating: 4.7, opening_hours: '全天开放（内部景点时间不一）'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (yanshuiya:Food {name: '盐水鸭', type: '金陵菜', price_range: '中', description: '皮白肉嫩，清淡爽口'}),
               (yaxuefansitang:Food {name: '鸭血粉丝汤', type: '小吃', price_range: '低', description: '鲜香爽滑，南京代表性风味'}),
               (jinlingfandian:Accommodation {name: '南京金陵饭店', type: '五星级酒店', price_range: '高', rating: 4.7}),
               (fuziamiaoyouth:Accommodation {name: '南京夫子庙国际青年旅舍', type: '经济型酒店', price_range: '低', rating: 4.5}),
               (nanjingmetro1:Transportation {name: '南京地铁1号线', type: '地铁', route: '迈皋桥-中国药科大学', price: '2-7元'}),
               (lukouairportbus:Transportation {name: '南京禄口国际机场大巴', type: '大巴', route: '机场-市区（南京站/南京南站）', price: '20元'})
           """)

            # 4. 创建关系：景点→城市
            session.run("""
               MATCH (a:Attraction), (c:City {name: '南京'})
               WHERE a.name IN ['中山陵', '夫子庙-秦淮风光带']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建关系：城市→推荐美食
            session.run("""
               MATCH (c:City {name: '南京'}), (f:Food)
               WHERE f.name IN ['盐水鸭', '鸭血粉丝汤']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建关系：景点→附近美食
            session.run("""
               MATCH (a:Attraction {name: '夫子庙-秦淮风光带'}), (f:Food {name: '鸭血粉丝汤'})
               CREATE (a)-[:NEAR_FOOD {distance: '街区内外众多老字号可品尝'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '夫子庙-秦淮风光带'}), (f:Food {name: '盐水鸭'})
               CREATE (a)-[:NEAR_FOOD {distance: '景区及市区老字号有售'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '中山陵'}), (f:Food)
               WHERE f.name IN ['盐水鸭', '鸭血粉丝汤']
               CREATE (a)-[:NEAR_FOOD {distance: '周边餐馆及市区可找到'}]->(f)
           """)

            # 7. 创建关系：景点→附近住宿
            session.run("""
               MATCH (a:Attraction {name: '中山陵'}), (ac:Accommodation)
               WHERE ac.name IN ['南京金陵饭店']
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '南京东郊国宾馆（距离约2km）'}]->(ac)
               
           """)
            session.run("""
               MATCH (a:Attraction {name: '夫子庙-秦淮风光带'}), (ac:Accommodation {name: '南京夫子庙国际青年旅舍'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '位于景区周边'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction), (ac:Accommodation)
               WHERE (a.name = '中山陵' AND ac.name = '南京夫子庙国际青年旅舍')
                  OR (a.name = '夫子庙-秦淮风光带' AND ac.name = '南京金陵饭店')
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '市区内交通可达'}]->(ac)
           """)

            # 8. 创建关系：城市→交通
            session.run("""
               MATCH (c:City {name: '南京'}), (t:Transportation)
               WHERE t.name IN ['南京地铁1号线', '南京禄口国际机场大巴']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)

        print("南京市旅游数据导入完成！")

    def import_wuxi_data(self):
        """导入无锡市旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (wuxi:City {name: '无锡', level: '新一线城市', description: '江苏省地级市，位于长江三角洲中心，被誉为“太湖明珠”、“江南水乡”，是中国民族工业和乡镇工业的摇篮，以优美的太湖风光和禅意文化闻名'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (lingshengjing:Attraction {name: '灵山胜境', type: '人文景观', rating: 4.8, opening_hours: '7:30-17:00'}),
               (yuantouzhu:Attraction {name: '鼋头渚', type: '自然景观', rating: 4.7, opening_hours: '8:00-17:00'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (jiangpaigu:Food {name: '无锡酱排骨', type: '本帮菜', price_range: '中', description: '色泽酱红，肉质酥烂，咸中带甜'}),
               (xiaolongbao:Food {name: '小笼包', type: '小吃', price_range: '低', description: '皮薄馅足，汤汁鲜甜，无锡特色'}),
               (taihufandian:Accommodation {name: '无锡太湖饭店', type: '五星级酒店', price_range: '高', rating: 4.6}),
               (junlaibinhu:Accommodation {name: '无锡君来湖滨饭店', type: '商务酒店', price_range: '中高', rating: 4.5}),
               (wuximetro1:Transportation {name: '无锡地铁1号线', type: '地铁', route: '堰桥-南方泉', price: '2-7元'}),
               (shuofangairportbus:Transportation {name: '无锡苏南硕放国际机场大巴', type: '大巴', route: '机场-市区（火车站）', price: '10-20元'})
           """)

            # 4. 创建关系：景点→城市
            session.run("""
               MATCH (a:Attraction), (c:City {name: '无锡'})
               WHERE a.name IN ['灵山胜境', '鼋头渚']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建关系：城市→推荐美食
            session.run("""
               MATCH (c:City {name: '无锡'}), (f:Food)
               WHERE f.name IN ['无锡酱排骨', '小笼包']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建关系：景点→附近美食
            session.run("""
               MATCH (a:Attraction), (f:Food {name: '无锡酱排骨'})
               WHERE a.name IN ['灵山胜境', '鼋头渚']
               CREATE (a)-[:NEAR_FOOD {distance: '惠山古镇等老街区可品尝正宗风味'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction), (f:Food {name: '小笼包'})
               WHERE a.name IN ['灵山胜境', '鼋头渚']
               CREATE (a)-[:NEAR_FOOD {distance: '景区周边及市区小吃店均有提供'}]->(f)
           """)

            # 7. 创建关系：景点→附近住宿
            session.run("""
               MATCH (a:Attraction {name: '鼋头渚'}), (ac:Accommodation {name: '无锡太湖饭店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '位于太湖畔，紧邻景区'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '灵山胜境'}), (ac:Accommodation {name: '无锡君来湖滨饭店'})
               CREATE (a)-[:NEAR_FOOD {distance: '市区及景区周边均有住宿选择'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction), (ac:Accommodation)
               WHERE (a.name = '鼋头渚' AND ac.name = '无锡君来湖滨饭店')
                  OR (a.name = '灵山胜境' AND ac.name = '无锡太湖饭店')
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '可通过公共交通抵达'}]->(ac)
           """)

            # 8. 创建关系：城市→交通
            session.run("""
               MATCH (c:City {name: '无锡'}), (t:Transportation)
               WHERE t.name IN ['无锡地铁1号线', '无锡苏南硕放国际机场大巴']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)

        print("无锡市旅游数据导入完成！")

    def import_xuzhou_data(self):
        """导入徐州市旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (xuzhou:City {name: '徐州', level: '二线城市', description: '江苏省地级市，全国重要的综合性交通枢纽和淮海经济区中心城市，历史文化悠久，被誉为“彭祖故国、刘邦故里、项羽故都”，素有“五省通衢”之称'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (yunlonghu:Attraction {name: '云龙湖风景区', type: '自然景观', rating: 4.7, opening_hours: '全天开放'}),
               (guishanhanmu:Attraction {name: '龟山汉墓', type: '人文景观', rating: 4.6, opening_hours: '8:30-17:00'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (diguoji:Food {name: '地锅鸡', type: '徐海菜', price_range: '中', description: '鸡肉鲜嫩，贴饼沾满汤汁，风味浓郁'}),
               (shitatang:Food {name: '饣它汤', type: '小吃', price_range: '低', description: '用母鸡、麦仁等熬制，鲜香辛辣，历史悠久'}),
               (suninghyatt:Accommodation {name: '徐州苏宁凯悦酒店', type: '五星级酒店', price_range: '高', rating: 4.6}),
               (kaiyuanmingdu:Accommodation {name: '徐州开元名都大酒店', type: '商务酒店', price_range: '中', rating: 4.4}),
               (xuzhoumetro1:Transportation {name: '徐州地铁1号线', type: '地铁', route: '路窝-徐州东站', price: '2-6元'}),
               (guanyinairportbus:Transportation {name: '徐州观音国际机场大巴', type: '大巴', route: '机场-市区（徐州站/徐州东站）', price: '20元'})
           """)

            # 4. 创建关系：景点→城市
            session.run("""
               MATCH (a:Attraction), (c:City {name: '徐州'})
               WHERE a.name IN ['云龙湖风景区', '龟山汉墓']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建关系：城市→推荐美食
            session.run("""
               MATCH (c:City {name: '徐州'}), (f:Food)
               WHERE f.name IN ['地锅鸡', '饣它汤']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建关系：景点→附近美食
            session.run("""
               MATCH (a:Attraction), (f:Food {name: '地锅鸡'})
               WHERE a.name IN ['云龙湖风景区', '龟山汉墓']
               CREATE (a)-[:NEAR_FOOD {distance: '市区内众多餐馆可品尝'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction), (f:Food {name: '饣它汤'})
               WHERE a.name IN ['云龙湖风景区', '龟山汉墓']
               CREATE (a)-[:NEAR_FOOD {distance: '市区早餐店及餐馆可提供'}]->(f)
           """)

            # 7. 创建关系：景点→附近住宿
            session.run("""
               MATCH (a:Attraction {name: '云龙湖风景区'}), (ac:Accommodation {name: '徐州开元名都大酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '约2km'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '龟山汉墓'}), (ac:Accommodation)
               WHERE ac.name IN ['徐州苏宁凯悦酒店', '徐州开元名都大酒店']
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '建议返回市区住宿'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '云龙湖风景区'}), (ac:Accommodation {name: '徐州苏宁凯悦酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '市区内交通可达'}]->(ac)
           """)

            # 8. 创建关系：城市→交通
            session.run("""
               MATCH (c:City {name: '徐州'}), (t:Transportation)
               WHERE t.name IN ['徐州地铁1号线', '徐州观音国际机场大巴']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)

        print("徐州市旅游数据导入完成！")

    def import_changzhou_data(self):
        """导入常州市旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (changzhou:City {name: '常州', level: '二线城市', description: '江苏省地级市，长江三角洲中心区城市，以现代装备制造和旅游产业闻名，被誉为“龙城”，是一座充满活力的工业与旅游创新之城'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (zhonghuakonglongyuan:Attraction {name: '中华恐龙园', type: '主题乐园', rating: 4.7, opening_hours: '9:00-17:00'}),
               (tianmuhu:Attraction {name: '天目湖旅游度假区', type: '自然景观', rating: 4.6, opening_hours: '全天开放（内部景点时间不一）'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (tianmuhuyutou:Food {name: '天目湖砂锅鱼头', type: '地方特色', price_range: '中高', description: '选用天目湖鳙鱼，汤色乳白，鲜美无比'}),
               (jiaxiexiaolongbao:Food {name: '加蟹小笼包', type: '小吃', price_range: '中', description: '蟹香浓郁，汤汁醇厚'}),
               (fuduVOCO:Accommodation {name: '常州富都VOCO酒店', type: '高端酒店', price_range: '高', rating: 4.7}),
               (konglongchengweijing:Accommodation {name: '常州环球恐龙城维景国际大酒店', type: '度假酒店', price_range: '中高', rating: 4.6}),
               (changzhoutmetro1:Transportation {name: '常州地铁1号线', type: '地铁', route: '森林公园-南夏墅', price: '2-7元'}),
               (benniuairportbus:Transportation {name: '常州奔牛国际机场大巴', type: '大巴', route: '机场-市区（常州客运中心）', price: '10-20元'})
           """)

            # 4. 创建关系：景点→城市
            session.run("""
               MATCH (a:Attraction), (c:City {name: '常州'})
               WHERE a.name IN ['中华恐龙园', '天目湖旅游度假区']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建关系：城市→推荐美食
            session.run("""
               MATCH (c:City {name: '常州'}), (f:Food)
               WHERE f.name IN ['天目湖砂锅鱼头', '加蟹小笼包']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建关系：景点→附近美食
            session.run("""
               MATCH (a:Attraction {name: '天目湖旅游度假区'}), (f:Food {name: '天目湖砂锅鱼头'})
               CREATE (a)-[:NEAR_FOOD {distance: '景区内可品尝最正宗风味'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '中华恐龙园'}), (f:Food {name: '加蟹小笼包'})
               CREATE (a)-[:NEAR_FOOD {distance: '度假区及市区餐馆可提供'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction), (f:Food)
               WHERE (a.name = '天目湖旅游度假区' AND f.name = '加蟹小笼包')
                  OR (a.name = '中华恐龙园' AND f.name = '天目湖砂锅鱼头')
               CREATE (a)-[:NEAR_FOOD {distance: '市区内可找到'}]->(f)
           """)

            # 7. 创建关系：景点→附近住宿
            session.run("""
               MATCH (a:Attraction {name: '中华恐龙园'}), (ac:Accommodation {name: '常州环球恐龙城维景国际大酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '位于度假区内'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '天目湖旅游度假区'}), (ac:Accommodation {name: '常州富都VOCO酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '建议选择景区周边住宿'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '天目湖旅游度假区'}), (ac:Accommodation)
               WHERE ac.name IN ['常州富都VOCO酒店']
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '市区高端选择，交通可达'}]->(ac)
           """)

            # 8. 创建关系：城市→交通
            session.run("""
               MATCH (c:City {name: '常州'}), (t:Transportation)
               WHERE t.name IN ['常州地铁1号线', '常州奔牛国际机场大巴']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)

        print("常州市旅游数据导入完成！")

    def import_suzhou_data(self):
        """导入苏州市旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (suzhou:City {name: '苏州', level: '新一线城市', description: '江苏省地级市，长江三角洲重要的中心城市之一，以其经典的江南园林和水乡古镇闻名于世，素有“人间天堂”、“东方威尼斯”的美誉'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (zhuozhengyuan:Attraction {name: '拙政园', type: '人文景观', rating: 4.7, opening_hours: '7:30-17:30'}),
               (pingjianglu:Attraction {name: '平江路', type: '人文景观', rating: 4.7, opening_hours: '全天开放'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (songshuguiyu:Food {name: '松鼠鳜鱼', type: '苏帮菜', price_range: '中高', description: '造型美观，外脆里嫩，酸甜可口'}),
               (yangchengdazhaxie:Food {name: '阳澄湖大闸蟹', type: '地方特产', price_range: '高', description: '蟹肉鲜美，蟹黄醇厚，秋季时令珍品'}),
               (nigrhotel:Accommodation {name: '苏州尼依格罗酒店', type: '五星级酒店', price_range: '高', rating: 4.8}),
               (pingjianghuafu:Accommodation {name: '苏州平江华府宾馆', type: '精品酒店', price_range: '中', rating: 4.6}),
               (suzhoumetro4:Transportation {name: '苏州地铁4号线', type: '地铁', route: '龙道浜-同里', price: '2-7元'}),
               (beiguangchangkeyun:Transportation {name: '苏州北广场汽车客运站', type: '大巴', route: '发往周庄、同里等水乡', price: '15-30元'})
           """)

            # 4. 创建关系：景点→城市
            session.run("""
               MATCH (a:Attraction), (c:City {name: '苏州'})
               WHERE a.name IN ['拙政园', '平江路']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建关系：城市→推荐美食
            session.run("""
               MATCH (c:City {name: '苏州'}), (f:Food)
               WHERE f.name IN ['松鼠鳜鱼', '阳澄湖大闸蟹']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建关系：景点→附近美食
            session.run("""
               MATCH (a:Attraction), (f:Food)
               WHERE a.name IN ['拙政园', '平江路']
                 AND f.name IN ['松鼠鳜鱼', '阳澄湖大闸蟹']
               CREATE (a)-[:NEAR_FOOD {distance: '观前街及平江路周边老字号可品尝'}]->(f)
           """)

            # 7. 创建关系：景点→附近住宿
            session.run("""
               MATCH (a:Attraction {name: '拙政园'}), (ac:Accommodation {name: '苏州平江华府宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '位于历史街区，步行可达'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '平江路'}), (ac:Accommodation {name: '苏州平江华府宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '紧邻景区，位置优越'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction), (ac:Accommodation {name: '苏州尼依格罗酒店'})
               WHERE a.name IN ['拙政园', '平江路']
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '市区高端选择，交通便捷'}]->(ac)
           """)

            # 8. 创建关系：城市→交通
            session.run("""
               MATCH (c:City {name: '苏州'}), (t:Transportation)
               WHERE t.name IN ['苏州地铁4号线', '苏州北广场汽车客运站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)

        print("苏州市旅游数据导入完成！")

    def import_nantong_data(self):
        """导入南通市旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (nantong:City {name: '南通', level: '二线城市', description: '江苏省地级市，位于长江入海口北翼，与中国经济中心上海隔江相望，被誉为“中国近代第一城”、“体育之乡”、“教育之乡”'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (langshan:Attraction {name: '狼山风景名胜区', type: '自然+人文景观', rating: 4.6, opening_hours: '8:00-17:00'}),
               (haohe:Attraction {name: '濠河风景名胜区', type: '自然+人文景观', rating: 4.5, opening_hours: '全天开放'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (nantongwenge:Food {name: '南通文蛤', type: '地方特色', price_range: '中', description: '肉质鲜嫩，有“天下第一鲜”之称'}),
               (gangpianbing:Food {name: '缸片饼', type: '小吃', price_range: '低', description: '传统烤制面食，香脆可口'}),
               (binjiangzhouji:Accommodation {name: '南通滨江洲际酒店', type: '五星级酒店', price_range: '高', rating: 4.6}),
               (nantongdafandian:Accommodation {name: '南通大饭店', type: '商务酒店', price_range: '中', rating: 4.4}),
               (nantongmetro1:Transportation {name: '南通地铁1号线', type: '地铁', route: '平潮-振兴路', price: '2-6元'}),
               (hutongtielu:Transportation {name: '沪通铁路', type: '高铁', route: '南通-上海', price: '50-80元'})
           """)

            # 4. 创建关系：景点→城市
            session.run("""
               MATCH (a:Attraction), (c:City {name: '南通'})
               WHERE a.name IN ['狼山风景名胜区', '濠河风景名胜区']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建关系：城市→推荐美食
            session.run("""
               MATCH (c:City {name: '南通'}), (f:Food)
               WHERE f.name IN ['南通文蛤', '缸片饼']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建关系：景点→附近美食
            session.run("""
               MATCH (a:Attraction {name: '濠河风景名胜区'}), (f:Food)
               WHERE f.name IN ['南通文蛤', '缸片饼']
               CREATE (a)-[:NEAR_FOOD {distance: '景区周边及江海美食街可品尝'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '狼山风景名胜区'}), (f:Food {name: '南通文蛤'})
               CREATE (a)-[:NEAR_FOOD {distance: '江鲜餐馆可提供新鲜文蛤'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '狼山风景名胜区'}), (f:Food {name: '缸片饼'})
               CREATE (a)-[:NEAR_FOOD {distance: '市区传统早点铺可找到'}]->(f)
           """)

            # 7. 创建关系：景点→附近住宿
            session.run("""
               MATCH (a:Attraction {name: '狼山风景名胜区'}), (ac:Accommodation {name: '南通滨江洲际酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '可远眺长江，位置优越'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '濠河风景名胜区'}), (ac:Accommodation)
               WHERE ac.name IN ['南通滨江洲际酒店', '南通大饭店']
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '市区住宿选择，交通便利'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '狼山风景名胜区'}), (ac:Accommodation {name: '南通大饭店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '市区商务选择，交通可达'}]->(ac)
           """)

            # 8. 创建关系：城市→交通
            session.run("""
               MATCH (c:City {name: '南通'}), (t:Transportation)
               WHERE t.name IN ['南通地铁1号线', '沪通铁路']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)

        print("南通市旅游数据导入完成！")

    def import_lianyungang_data(self):
        """导入连云港市旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (lianyungang:City {name: '连云港', level: '三线城市', description: '江苏省地级市，中国首批沿海开放城市之一，是新亚欧大陆桥东方桥头堡，以《西游记》文化发源地闻名，被誉为“东海第一胜境”'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (huaguoshan:Attraction {name: '花果山', type: '自然+人文景观', rating: 4.5, opening_hours: '8:00-17:00'}),
               (liandao:Attraction {name: '连岛海滨度假区', type: '自然景观', rating: 4.4, opening_hours: '8:30-17:30'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (haixianshaokao:Food {name: '海鲜烧烤', type: '地方特色', price_range: '中', description: '黄海盛产各类海鲜，现捞现烤，鲜美无比'}),
               (doudan:Food {name: '豆丹', type: '地方特色', price_range: '中高', description: '连云港特色昆虫美食，口感独特，蛋白质丰富'}),
               (suningsofitel:Accommodation {name: '连云港苏宁索菲特酒店', type: '五星级酒店', price_range: '高', rating: 4.6}),
               (shenzhoubinguan:Accommodation {name: '连云港神州宾馆', type: '商务酒店', price_range: '中', rating: 4.3}),
               (brt:Transportation {name: '连云港BRT快速公交', type: '快速公交', route: '连接连云区与海州区', price: '1-4元'}),
               (baitaairportbus:Transportation {name: '连云港白塔埠机场大巴', type: '大巴', route: '机场-市区', price: '15元'})
           """)

            # 4. 创建关系：景点→城市
            session.run("""
               MATCH (a:Attraction), (c:City {name: '连云港'})
               WHERE a.name IN ['花果山', '连岛海滨度假区']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建关系：城市→推荐美食
            session.run("""
               MATCH (c:City {name: '连云港'}), (f:Food)
               WHERE f.name IN ['海鲜烧烤', '豆丹']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建关系：景点→附近美食
            session.run("""
               MATCH (a:Attraction {name: '连岛海滨度假区'}), (f:Food {name: '海鲜烧烤'})
               CREATE (a)-[:NEAR_FOOD {distance: '景区内及盐河巷美食街可品尝'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '花果山'}), (f:Food {name: '海鲜烧烤'})
               CREATE (a)-[:NEAR_FOOD {distance: '市区盐河巷美食街可找到'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction), (f:Food {name: '豆丹'})
               WHERE a.name IN ['花果山', '连岛海滨度假区']
               CREATE (a)-[:NEAR_FOOD {distance: '市区特色餐馆可体验'}]->(f)
           """)

            # 7. 创建关系：景点→附近住宿
            session.run("""
               MATCH (a:Attraction {name: '花果山'}), (ac:Accommodation {name: '连云港神州宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '距离景区较近'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '连岛海滨度假区'}), (ac:Accommodation)
               WHERE ac.name IN ['连云港苏宁索菲特酒店', '连云港神州宾馆']
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '建议选择连云区住宿'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '花果山'}), (ac:Accommodation {name: '连云港苏宁索菲特酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '市区高端选择，交通可达'}]->(ac)
           """)

            # 8. 创建关系：城市→交通
            session.run("""
               MATCH (c:City {name: '连云港'}), (t:Transportation)
               WHERE t.name IN ['连云港BRT快速公交', '连云港白塔埠机场大巴']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)

        print("连云港市旅游数据导入完成！")

    def import_huaian_data(self):
        """导入淮安市旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (huaian:City {name: '淮安', level: '三线城市', description: '江苏省地级市，国家历史文化名城，是江淮流域古文化发源地之一，被誉为“中国运河之都”，是伟人周恩来总理的故乡'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (zhouenlai:Attraction {name: '周恩来故里旅游景区', type: '人文景观', rating: 4.8, opening_hours: '9:00-17:00'}),
               (liyunhe:Attraction {name: '里运河文化长廊', type: '人文景观', rating: 4.5, opening_hours: '全天开放（游船时间另计）'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (ruandouchangyu:Food {name: '软兜长鱼', type: '淮扬菜', price_range: '中', description: '选用笔杆青鳝鱼脊背肉，软嫩鲜香，是淮扬菜代表作'}),
               (pingqiaodoufu:Food {name: '平桥豆腐', type: '淮扬菜', price_range: '中低', description: '刀工精细，羹汤醇厚，鲜美滑嫩'}),
               (guolian奥体:Accommodation {name: '淮安国联奥体名都酒店', type: '高端酒店', price_range: '中高', rating: 4.5}),
               (shuguanghotel:Accommodation {name: '淮安曙光国际大酒店', type: '商务酒店', price_range: '中', rating: 4.3}),
               (youguidianche:Transportation {name: '淮安有轨电车T1线', type: '有轨电车', route: '体育馆-淮安区', price: '2元'}),
               (lianshuiairportbus:Transportation {name: '淮安涟水国际机场大巴', type: '大巴', route: '机场-市区', price: '20元'})
           """)

            # 4. 创建关系：景点→城市
            session.run("""
               MATCH (a:Attraction), (c:City {name: '淮安'})
               WHERE a.name IN ['周恩来故里旅游景区', '里运河文化长廊']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建关系：城市→推荐美食
            session.run("""
               MATCH (c:City {name: '淮安'}), (f:Food)
               WHERE f.name IN ['软兜长鱼', '平桥豆腐']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建关系：景点→附近美食
            session.run("""
               MATCH (a:Attraction), (f:Food)
               WHERE a.name IN ['周恩来故里旅游景区', '里运河文化长廊']
                 AND f.name IN ['软兜长鱼', '平桥豆腐']
               CREATE (a)-[:NEAR_FOOD {distance: '河下古镇及文楼可体验经典淮扬菜'}]->(f)
           """)

            # 7. 创建关系：景点→附近住宿
            session.run("""
               MATCH (a:Attraction {name: '周恩来故里旅游景区'}), (ac:Accommodation {name: '淮安曙光国际大酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '距离约4km'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '里运河文化长廊'}), (ac:Accommodation)
               WHERE ac.name IN ['淮安国联奥体名都酒店', '淮安曙光国际大酒店']
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '运河沿线住宿选择，交通便利'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '周恩来故里旅游景区'}), (ac:Accommodation {name: '淮安国联奥体名都酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '市区高端选择，交通可达'}]->(ac)
           """)

            # 8. 创建关系：城市→交通
            session.run("""
               MATCH (c:City {name: '淮安'}), (t:Transportation)
               WHERE t.name IN ['淮安有轨电车T1线', '淮安涟水国际机场大巴']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)

        print("淮安市旅游数据导入完成！")

    def import_yancheng_data(self):
        """导入盐城市旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (yancheng:City {name: '盐城', level: '三线城市', description: '江苏省地级市，拥有江苏省最长的海岸线，是“东方湿地之都”，以广袤的滩涂湿地和“麋鹿故乡”、“丹顶鹤家园”闻名于世'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (miluyuan:Attraction {name: '中华麋鹿园', type: '自然景观', rating: 4.7, opening_hours: '8:30-17:00'}),
               (dandinghe:Attraction {name: '丹顶鹤湿地生态旅游区', type: '自然景观', rating: 4.6, opening_hours: '8:30-17:00'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (dongtaiyutangmian:Food {name: '东台鱼汤面', type: '地方特色', price_range: '低', description: '汤色乳白，汤汁醇厚，面条爽滑，鲜美滋补'}),
               (huitubiao:Food {name: '烩土膘', type: '地方特色', price_range: '中', description: '用猪肉皮深度烹制的传统菜肴，口感软糯'}),
               (wanhaohotel:Accommodation {name: '盐城万豪酒店', type: '五星级酒店', price_range: '高', rating: 4.6}),
               (gangfuzhouji:Accommodation {name: '盐城港府洲际酒店', type: '商务酒店', price_range: '中', rating: 4.4}),
               (srt1:Transportation {name: '盐城SRT一号线', type: '超级虚拟轨道列车', route: '先锋岛-东环路', price: '1元'}),
               (nanyangairportbus:Transportation {name: '盐城南洋国际机场大巴', type: '大巴', route: '机场-市区', price: '15元'})
           """)

            # 4. 创建关系：景点→城市
            session.run("""
               MATCH (a:Attraction), (c:City {name: '盐城'})
               WHERE a.name IN ['中华麋鹿园', '丹顶鹤湿地生态旅游区']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建关系：城市→推荐美食
            session.run("""
               MATCH (c:City {name: '盐城'}), (f:Food)
               WHERE f.name IN ['东台鱼汤面', '烩土膘']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建关系：景点→附近美食
            session.run("""
               MATCH (a:Attraction), (f:Food {name: '东台鱼汤面'})
               WHERE a.name IN ['中华麋鹿园', '丹顶鹤湿地生态旅游区']
               CREATE (a)-[:NEAR_FOOD {distance: '返回市区或大丰区早餐店可品尝'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction), (f:Food {name: '烩土膘'})
               WHERE a.name IN ['中华麋鹿园', '丹顶鹤湿地生态旅游区']
               CREATE (a)-[:NEAR_FOOD {distance: '市区老字号餐馆可体验'}]->(f)
           """)

            # 7. 创建关系：景点→附近住宿
            session.run("""
               MATCH (a:Attraction), (ac:Accommodation)
               WHERE a.name IN ['中华麋鹿园', '丹顶鹤湿地生态旅游区']
                 AND ac.name IN ['盐城万豪酒店', '盐城港府洲际酒店']
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '需返回市区或大丰区住宿'}]->(ac)
           """)

            # 8. 创建关系：城市→交通
            session.run("""
               MATCH (c:City {name: '盐城'}), (t:Transportation)
               WHERE t.name IN ['盐城SRT一号线', '盐城南洋国际机场大巴']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)

        print("盐城市旅游数据导入完成！")

    def import_yangzhou_data(self):
        """导入扬州市旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (yangzhou:City {name: '扬州', level: '三线城市', description: '江苏省地级市，中国首批历史文化名城，因“淮左名都，竹西佳处”而闻名，是中国大运河联合申遗的牵头城市，素有“中国运河第一城”的美誉'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (shouxihu:Attraction {name: '瘦西湖', type: '自然+人文景观', rating: 4.7, opening_hours: '6:00-17:30'}),
               (geyuan:Attraction {name: '个园', type: '人文景观', rating: 4.6, opening_hours: '7:15-17:15'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (yangzhouchaofan:Food {name: '扬州炒饭', type: '淮扬菜', price_range: '中', description: '选料严谨，制作精细，颗粒分明，鲜嫩滑爽'}),
               (xiehuangtangbao:Food {name: '蟹黄汤包', type: '小吃', price_range: '中', description: '皮薄如纸，汤汁饱满，蟹香浓郁'}),
               (yingbinguan:Accommodation {name: '扬州迎宾馆', type: '国宾馆', price_range: '高', rating: 4.8}),
               (hongqiaofang:Accommodation {name: '扬州虹桥坊温泉酒店', type: '度假酒店', price_range: '中高', rating: 4.6}),
               (lvyouzhuanxian:Transportation {name: '扬州旅游专线', type: '公交', route: '连接主要景点', price: '2元'}),
               (taizhouairportbus:Transportation {name: '扬州泰州国际机场大巴', type: '大巴', route: '机场-市区', price: '25元'})
           """)

            # 4. 创建关系：景点→城市
            session.run("""
               MATCH (a:Attraction), (c:City {name: '扬州'})
               WHERE a.name IN ['瘦西湖', '个园']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建关系：城市→推荐美食
            session.run("""
               MATCH (c:City {name: '扬州'}), (f:Food)
               WHERE f.name IN ['扬州炒饭', '蟹黄汤包']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建关系：景点→附近美食
            session.run("""
               MATCH (a:Attraction), (f:Food)
               WHERE a.name IN ['瘦西湖', '个园']
                 AND f.name IN ['扬州炒饭', '蟹黄汤包']
               CREATE (a)-[:NEAR_FOOD {distance: '冶春茶社、富春茶社等老字号可体验'}]->(f)
           """)

            # 7. 创建关系：景点→附近住宿
            session.run("""
               MATCH (a:Attraction {name: '瘦西湖'}), (ac:Accommodation {name: '扬州迎宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '与景区毗邻，位置绝佳'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '瘦西湖'}), (ac:Accommodation {name: '扬州虹桥坊温泉酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '景区周边度假选择'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '个园'}), (ac:Accommodation)
               WHERE ac.name IN ['扬州迎宾馆', '扬州虹桥坊温泉酒店']
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '市区内交通便捷可达'}]->(ac)
           """)

            # 8. 创建关系：城市→交通
            session.run("""
               MATCH (c:City {name: '扬州'}), (t:Transportation)
               WHERE t.name IN ['扬州旅游专线', '扬州泰州国际机场大巴']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)

        print("扬州市旅游数据导入完成！")

    def import_zhenjiang_data(self):
        """导入镇江市旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (zhenjiang:City {name: '镇江', level: '三线城市', description: '江苏省地级市，位于长江与京杭大运河“十字黄金水道”交汇处，是江南著名的鱼米之乡，以“城市山林”和“天下第一江山”著称'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (jinshansi:Attraction {name: '金山寺', type: '人文景观', rating: 4.6, opening_hours: '8:00-17:00'}),
               (xijindu:Attraction {name: '西津渡古街', type: '人文景观', rating: 4.7, opening_hours: '全天开放（内部景点时间不一）'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (guogaimian:Food {name: '镇江锅盖面', type: '地方特色', price_range: '低', description: '面条筋道，汤底鲜美，因小锅盖煮面而得名'}),
               (yaorou:Food {name: '镇江肴肉', type: '冷菜', price_range: '中低', description: '水晶般莹润，肉质酥嫩，佐以姜丝和香醋风味更佳'}),
               (zhaohuang皇冠:Accommodation {name: '镇江兆和皇冠假日酒店', type: '五星级酒店', price_range: '高', rating: 4.5}),
               (guojifandian:Accommodation {name: '镇江国际饭店', type: '商务酒店', price_range: '中', rating: 4.3}),
               (gongjiao2:Transportation {name: '镇江公交2路', type: '公交', route: '途经金山、西津渡等主要景点', price: '1-2元'}),
               (zhenjiangnanzhan:Transportation {name: '镇江南站（高铁站）', type: '高铁', route: '连通南京、上海等长三角主要城市', price: '依里程而定'})
           """)

            # 4. 创建关系：景点→城市
            session.run("""
               MATCH (a:Attraction), (c:City {name: '镇江'})
               WHERE a.name IN ['金山寺', '西津渡古街']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建关系：城市→推荐美食
            session.run("""
               MATCH (c:City {name: '镇江'}), (f:Food)
               WHERE f.name IN ['镇江锅盖面', '镇江肴肉']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建关系：景点→附近美食
            session.run("""
               MATCH (a:Attraction {name: '西津渡古街'}), (f:Food)
               WHERE f.name IN ['镇江锅盖面', '镇江肴肉']
               CREATE (a)-[:NEAR_FOOD {distance: '古街及周边老字号可品尝'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '金山寺'}), (f:Food {name: '镇江锅盖面'})
               CREATE (a)-[:NEAR_FOOD {distance: '景区周边餐馆可提供'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '金山寺'}), (f:Food {name: '镇江肴肉'})
               CREATE (a)-[:NEAR_FOOD {distance: '市区餐馆搭配香醋食用更佳'}]->(f)
           """)

            # 7. 创建关系：景点→附近住宿
            session.run("""
               MATCH (a:Attraction {name: '金山寺'}), (ac:Accommodation {name: '镇江兆和皇冠假日酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '约3km'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '西津渡古街'}), (ac:Accommodation)
               WHERE ac.name IN ['镇江兆和皇冠假日酒店', '镇江国际饭店']
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '市区住宿，交通便利'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '金山寺'}), (ac:Accommodation {name: '镇江国际饭店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '市区商务选择，交通可达'}]->(ac)
           """)

            # 8. 创建关系：城市→交通
            session.run("""
               MATCH (c:City {name: '镇江'}), (t:Transportation)
               WHERE t.name IN ['镇江公交2路', '镇江南站（高铁站）']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)

        print("镇江市旅游数据导入完成！")

    def import_taizhou_data(self):
        """导入泰州市旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (taizhou:City {name: '泰州', level: '三线城市', description: '江苏省地级市，是承南启北的水陆要津，为苏中门户。这里人文荟萃，是京剧大师梅兰芳的故乡，也是中国著名的“水产之乡”和“祥瑞福地”'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (qinhu:Attraction {name: '溱湖国家湿地公园', type: '自然景观', rating: 4.6, opening_hours: '8:30-17:00'}),
               (fengchenghe:Attraction {name: '凤城河风景区', type: '自然+人文景观', rating: 4.5, opening_hours: '全天开放（内部景点时间不一）'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (taizhouzaocha:Food {name: '泰州早茶', type: '地方特色', price_range: '中低', description: '以烫干丝、鱼汤面、蟹黄包为代表，讲究“早茶三宝”'}),
               (qinhu baxian:Food {name: '溱湖八鲜', type: '地方特色', price_range: '中', description: '汇聚溱湖出产的簖蟹、甲鱼、银鱼等八种水产品，鲜美无比'}),
               (wandajiahua:Accommodation {name: '泰州万达嘉华酒店', type: '五星级酒店', price_range: '高', rating: 4.5}),
               (guojijinling:Accommodation {name: '泰州国际金陵大酒店', type: '商务酒店', price_range: '中', rating: 4.3}),
               (you1xian:Transportation {name: '泰州公交游1线', type: '公交', route: '连接市区主要景点', price: '1-2元'}),
               (taizhouzhan:Transportation {name: '泰州站（高铁站）', type: '高铁', route: '连通北京、上海、南京等地', price: '依里程而定'})
           """)

            # 4. 创建关系：景点→城市
            session.run("""
               MATCH (a:Attraction), (c:City {name: '泰州'})
               WHERE a.name IN ['溱湖国家湿地公园', '凤城河风景区']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建关系：城市→推荐美食
            session.run("""
               MATCH (c:City {name: '泰州'}), (f:Food)
               WHERE f.name IN ['泰州早茶', '溱湖八鲜']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建关系：景点→附近美食
            session.run("""
               MATCH (a:Attraction {name: '凤城河风景区'}), (f:Food {name: '泰州早茶'})
               CREATE (a)-[:NEAR_FOOD {distance: '凤城河畔老街可体验早茶文化'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '溱湖国家湿地公园'}), (f:Food {name: '溱湖八鲜'})
               CREATE (a)-[:NEAR_FOOD {distance: '景区周边餐馆可品尝新鲜水产'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction), (f:Food)
               WHERE (a.name = '凤城河风景区' AND f.name = '溱湖八鲜')
                  OR (a.name = '溱湖国家湿地公园' AND f.name = '泰州早茶')
               CREATE (a)-[:NEAR_FOOD {distance: '市区餐馆可找到'}]->(f)
           """)

            # 7. 创建关系：景点→附近住宿
            session.run("""
               MATCH (a:Attraction {name: '溱湖国家湿地公园'}), (ac:Accommodation)
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '溱湖度假村（位于景区附近）'}]->(ac)
               WHERE ac.name IN ['泰州万达嘉华酒店']
           """)
            session.run("""
               MATCH (a:Attraction {name: '凤城河风景区'}), (ac:Accommodation)
               WHERE ac.name IN ['泰州万达嘉华酒店', '泰州国际金陵大酒店']
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '景区周边住宿选择丰富'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '溱湖国家湿地公园'}), (ac:Accommodation {name: '泰州国际金陵大酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '建议返回市区住宿'}]->(ac)
           """)

            # 8. 创建关系：城市→交通
            session.run("""
               MATCH (c:City {name: '泰州'}), (t:Transportation)
               WHERE t.name IN ['泰州公交游1线', '泰州站（高铁站）']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)

        print("泰州市数据导入完成！")

    def import_suqian_data(self):
        """导入宿迁市旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (suqian:City {name: '宿迁', level: '三线城市', description: '江苏省地级市，位于江苏省北部，是西楚霸王项羽的故乡，也是中国酒文化的发源地之一，被誉为“项王故里”、“中国酒都”、“水韵之城”'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (xiangwangguli:Attraction {name: '项王故里', type: '人文景观', rating: 4.5, opening_hours: '9:00-17:30'}),
               (santaishan:Attraction {name: '三台山国家森林公园', type: '自然景观', rating: 4.6, opening_hours: '9:00-17:30'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (huanggouzutourou:Food {name: '黄狗猪头肉', type: '地方特色', price_range: '中', description: '色泽红亮，香糯浓醇，肥而不腻，是宿迁传统名菜'}),
               (chelunbing:Food {name: '车轮饼', type: '小吃', price_range: '低', description: '外形似车轮，外皮酥脆，内馅香甜'}),
               (henglihotel:Accommodation {name: '宿迁恒力国际大酒店', type: '五星级酒店', price_range: '高', rating: 4.6}),
               (fenghuazhili:Accommodation {name: '宿迁枫华丽致酒店', type: '商务酒店', price_range: '中', rating: 4.4}),
               (you1lu:Transportation {name: '宿迁公交游1路', type: '公交', route: '连接项王故里、三台山等主要景点', price: '1-2元'}),
               (keyunzhanbanche:Transportation {name: '宿迁客运站班车', type: '大巴', route: '连通南京、徐州等周边城市', price: '依里程而定'})
           """)

            # 4. 创建关系：景点→城市
            session.run("""
               MATCH (a:Attraction), (c:City {name: '宿迁'})
               WHERE a.name IN ['项王故里', '三台山国家森林公园']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建关系：城市→推荐美食
            session.run("""
               MATCH (c:City {name: '宿迁'}), (f:Food)
               WHERE f.name IN ['黄狗猪头肉', '车轮饼']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建关系：景点→附近美食
            session.run("""
               MATCH (a:Attraction {name: '项王故里'}), (f:Food)
               WHERE f.name IN ['黄狗猪头肉', '车轮饼']
               CREATE (a)-[:NEAR_FOOD {distance: '景区周边及老街可品尝地道风味'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '三台山国家森林公园'}), (f:Food {name: '车轮饼'})
               CREATE (a)-[:NEAR_FOOD {distance: '景区服务区及市区可找到'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '三台山国家森林公园'}), (f:Food {name: '黄狗猪头肉'})
               CREATE (a)-[:NEAR_FOOD {distance: '建议返回市区品尝正宗口味'}]->(f)
           """)

            # 7. 创建关系：景点→附近住宿
            session.run("""
               MATCH (a:Attraction {name: '三台山国家森林公园'}), (ac:Accommodation)
               WHERE ac.name IN ['宿迁恒力国际大酒店']
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '三台山衲田村酒店（位于景区内）'}]->(ac)
               
           """)
            session.run("""
               MATCH (a:Attraction {name: '项王故里'}), (ac:Accommodation)
               WHERE ac.name IN ['宿迁恒力国际大酒店', '宿迁枫华丽致酒店']
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '市区住宿选择，交通便利'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '三台山国家森林公园'}), (ac:Accommodation {name: '宿迁枫华丽致酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '市区商务选择，交通可达'}]->(ac)
           """)

            # 8. 创建关系：城市→交通
            session.run("""
               MATCH (c:City {name: '宿迁'}), (t:Transportation)
               WHERE t.name IN ['宿迁公交游1路', '宿迁客运站班车']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)

        print("宿迁市旅游数据导入完成！")

    def import_jiangyin_data(self):
        """导入江阴市旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (jiangyin:City {name: '江阴', level: '县级市（由无锡市代管）', description: '位于江苏省南部，因地处“大江之阴”而得名，是长江下游重要的滨江港口城市和交通枢纽，被誉为“江海门户”、“锁航要塞”，是“中国制造业第一县”'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (huangshanhu:Attraction {name: '江阴黄山湖公园', type: '自然+人文景观', rating: 4.5, opening_hours: '全天开放'}),
               (xuezhengwenhua:Attraction {name: '学政文化旅游区', type: '人文景观', rating: 4.4, opening_hours: '8:30-17:00'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (jiangyinhuntun:Food {name: '江阴河豚', type: '地方特色', price_range: '中高', description: '烹制技艺精湛，肉质鲜美，有“拼死吃河豚”之说'}),
               (matisu:Food {name: '马蹄酥', type: '传统茶食', price_range: '低', description: '酥香松软，甜而不腻，是当地传统名点'}),
               (huangjiaxilaideng:Accommodation {name: '江阴黄嘉喜来登酒店', type: '五星级酒店', price_range: '高', rating: 4.6}),
               (hongshengyuan:Accommodation {name: '江阴泓昇苑酒店', type: '商务酒店', price_range: '中', rating: 4.4}),
               (jiangyinqiche:Transportation {name: '江阴公交线路', type: '公交', route: '覆盖全市', price: '1-2元'}),
               (jiangyinkeyun:Transportation {name: '江阴客运站', type: '大巴', route: '频繁往返无锡、上海、苏州等周边城市', price: '依里程而定'})
           """)

            # 4. 创建关系：景点→城市
            session.run("""
               MATCH (a:Attraction), (c:City {name: '江阴'})
               WHERE a.name IN ['江阴黄山湖公园', '学政文化旅游区']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建关系：城市→推荐美食
            session.run("""
               MATCH (c:City {name: '江阴'}), (f:Food)
               WHERE f.name IN ['江阴河豚', '马蹄酥']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建关系：景点→附近美食
            session.run("""
               MATCH (a:Attraction), (f:Food {name: '江阴河豚'})
               WHERE a.name IN ['江阴黄山湖公园', '学政文化旅游区']
               CREATE (a)-[:NEAR_FOOD {distance: '市内专营河豚餐馆可体验'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction), (f:Food {name: '马蹄酥'})
               WHERE a.name IN ['江阴黄山湖公园', '学政文化旅游区']
               CREATE (a)-[:NEAR_FOOD {distance: '景区周边及传统糕点店有售'}]->(f)
           """)

            # 7. 创建关系：景点→附近住宿
            session.run("""
               MATCH (a:Attraction {name: '江阴黄山湖公园'}), (ac:Accommodation {name: '江阴黄嘉喜来登酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '位于江边，邻近公园'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '学政文化旅游区'}), (ac:Accommodation)
               WHERE ac.name IN ['江阴黄嘉喜来登酒店', '江阴泓昇苑酒店']
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '市区住宿，交通便捷'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '江阴黄山湖公园'}), (ac:Accommodation {name: '江阴泓昇苑酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '市区商务选择，交通可达'}]->(ac)
           """)

            # 8. 创建关系：城市→交通
            session.run("""
               MATCH (c:City {name: '江阴'}), (t:Transportation)
               WHERE t.name IN ['江阴公交线路', '江阴客运站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)

        print("江阴市旅游数据导入完成！")

    def import_yixing_data(self):
        """导入宜兴市旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (yixing:City {name: '宜兴', level: '县级市（由无锡市代管）', description: '位于江苏省南端，苏浙皖三省交界处，是闻名中外的“中国陶都”，以紫砂壶闻名天下，同时拥有丰富的竹海、茶洲、溶洞资源，素有“陶的古都，洞的世界，茶的绿洲，竹的海洋”之美誉'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (shanjuan:Attraction {name: '善卷洞', type: '自然景观', rating: 4.6, opening_hours: '8:00-16:30'}),
               (zhuhai:Attraction {name: '宜兴竹海风景区', type: '自然景观', rating: 4.6, opening_hours: '8:00-16:30'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (wumifan:Food {name: '宜兴乌米饭', type: '地方特色', price_range: '低', description: '用乌桕树叶汁浸泡糯米蒸制，油亮清香'}),
               (hengshanyutou:Food {name: '横山鱼头', type: '地方特色', price_range: '中', description: '选自横山水库的鳙鱼，鱼头硕大，肉质肥嫩，毫无土腥味'}),
               (aimeihotel:Accommodation {name: '宜兴艾美酒店', type: '度假酒店', price_range: '高', rating: 4.7}),
               (yixingbinguan:Accommodation {name: '宜兴宾馆', type: '商务酒店', price_range: '中', rating: 4.4}),
               (yixinglvyou:Transportation {name: '宜兴旅游专线', type: '公交', route: '连接市区与主要景点', price: '2-5元'}),
               (yixinggaotie:Transportation {name: '宜兴高铁站', type: '高铁', route: '宁杭高铁线，连通杭州、南京等地', price: '依里程而定'})
           """)

            # 4. 创建关系：景点→城市
            session.run("""
               MATCH (a:Attraction), (c:City {name: '宜兴'})
               WHERE a.name IN ['善卷洞', '宜兴竹海风景区']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建关系：城市→推荐美食
            session.run("""
               MATCH (c:City {name: '宜兴'}), (f:Food)
               WHERE f.name IN ['宜兴乌米饭', '横山鱼头']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建关系：景点→附近美食
            session.run("""
               MATCH (a:Attraction {name: '宜兴竹海风景区'}), (f:Food)
               WHERE f.name IN ['宜兴乌米饭', '横山鱼头']
               CREATE (a)-[:NEAR_FOOD {distance: '景区周边农家乐可品尝地道风味'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '善卷洞'}), (f:Food)
               WHERE f.name IN ['宜兴乌米饭', '横山鱼头']
               CREATE (a)-[:NEAR_FOOD {distance: '景区周边餐馆及农家乐提供'}]->(f)
           """)

            # 7. 创建关系：景点→附近住宿
            session.run("""
               MATCH (a:Attraction {name: '善卷洞'}), (ac:Accommodation {name: '宜兴艾美酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '位于云湖风景区，邻近景点'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '宜兴竹海风景区'}), (ac:Accommodation)
               WHERE ac.name IN ['宜兴艾美酒店', '宜兴宾馆']
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '景区周边度假住宿选择丰富'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '善卷洞'}), (ac:Accommodation {name: '宜兴宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '市区商务选择，交通可达'}]->(ac)
           """)

            # 8. 创建关系：城市→交通
            session.run("""
               MATCH (c:City {name: '宜兴'}), (t:Transportation)
               WHERE t.name IN ['宜兴旅游专线', '宜兴高铁站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)

        print("宜兴市旅游数据导入完成！")

    def import_liyang_data(self):
        """导入溧阳市旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (liyang:City {name: '溧阳', level: '县级市（由常州市代管）', description: '位于江苏省南部，苏、浙、皖三省交界处，是著名的“鱼米之乡”、“丝绸之乡”，以天目湖的秀美风光闻名，被誉为“江南明珠”'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (tianmuhu_liyang:Attraction {name: '天目湖旅游度假区', type: '自然景观', rating: 4.7, opening_hours: '8:30-17:00'}),
               (nanshanzhuhai:Attraction {name: '南山竹海', type: '自然景观', rating: 4.6, opening_hours: '8:30-17:00'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (tianmuhu_yutou_liyang:Food {name: '天目湖砂锅鱼头', type: '地方特色', price_range: '中高', description: '选用天目湖鳙鱼，汤色乳白，鲜美无比，是溧阳标志性美食'}),
               (wumifan_liyang:Food {name: '乌米饭', type: '地方特色', price_range: '低', description: '用乌桕树叶汁浸泡糯米蒸制，清香油润'}),
               (hantiandujia:Accommodation {name: '溧阳涵田度假村', type: '度假酒店', price_range: '高', rating: 4.7}),
               (wei_tianmuhu:Accommodation {name: '溧阳WEI天目湖酒店', type: '高端度假酒店', price_range: '高', rating: 4.8}),
               (liyanglvyou:Transportation {name: '溧阳旅游专线', type: '公交', route: '连接市区与天目湖、南山竹海', price: '3-8元'}),
               (liyanggaotie:Transportation {name: '溧阳站', type: '高铁', route: '宁杭高铁线，连通杭州、南京等地'})
           """)

            # 4. 创建关系：景点→城市
            session.run("""
               MATCH (a:Attraction), (c:City {name: '溧阳'})
               WHERE a.name IN ['天目湖旅游度假区', '南山竹海']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建关系：城市→推荐美食
            session.run("""
               MATCH (c:City {name: '溧阳'}), (f:Food)
               WHERE f.name IN ['天目湖砂锅鱼头', '乌米饭']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建关系：景点→附近美食
            session.run("""
               MATCH (a:Attraction {name: '天目湖旅游度假区'}), (f:Food {name: '天目湖砂锅鱼头'})
               CREATE (a)-[:NEAR_FOOD {distance: '景区内餐馆为最佳品尝地点'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction), (f:Food {name: '乌米饭'})
               WHERE a.name IN ['天目湖旅游度假区', '南山竹海']
               CREATE (a)-[:NEAR_FOOD {distance: '景区周边农家乐及餐馆可提供'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '南山竹海'}), (f:Food {name: '天目湖砂锅鱼头'})
               CREATE (a)-[:NEAR_FOOD {distance: '建议前往天目湖景区品尝正宗风味'}]->(f)
           """)

            # 7. 创建关系：景点→附近住宿
            session.run("""
               MATCH (a:Attraction {name: '天目湖旅游度假区'}), (ac:Accommodation {name: '溧阳涵田度假村'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '位于天目湖畔，紧邻景区'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '天目湖旅游度假区'}), (ac:Accommodation {name: '溧阳WEI天目湖酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '天目湖周边高端度假选择'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '南山竹海'}), (ac:Accommodation)
               WHERE ac.name IN ['溧阳涵田度假村', '溧阳WEI天目湖酒店']
               CREATE (a)-[:NEAR_FOOD {distance: '建议选择景区周边度假住宿'}]->(ac)
           """)

            # 8. 创建关系：城市→交通
            session.run("""
               MATCH (c:City {name: '溧阳'}), (t:Transportation)
               WHERE t.name IN ['溧阳旅游专线', '溧阳站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)

        print("溧阳市旅游数据导入完成！")

    def import_changshu_data(self):
        """导入常熟市旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (changshu:City {name: '常熟', level: '县级市（由苏州市代管）', description: '位于江苏省东南部，因“土壤膏沃，岁无水旱”而得名，是国家级历史文化名城，被誉为“江南福地”。经济发达，是中国重要的纺织服装基地。'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (shajiabang:Attraction {name: '沙家浜·虞山尚湖旅游区', type: '自然+人文+红色旅游', rating: 4.7, opening_hours: '8:00-16:30'}),
               (fangtayuan:Attraction {name: '方塔园', type: '人文景观', rating: 4.4, opening_hours: '8:00-16:30'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (jiaohuaji:Food {name: '叫化鸡', type: '地方特色', price_range: '中', description: '泥煨技法，鸡肉酥烂脱骨，香气扑鼻'}),
               (xunyoumian:Food {name: '蕈油面', type: '小吃', price_range: '中低', description: '用虞山特产松树蕈熬制的蕈油作浇头，鲜美异常'}),
               (rixinguoji:Accommodation {name: '常熟日航国际酒店', type: '五星级酒店', price_range: '高', rating: 4.6}),
               (yueshanxuan:Accommodation {name: '常熟阅山轩假日休闲酒店', type: '度假酒店', price_range: '中高', rating: 4.5}),
               (changshugongjiao:Transportation {name: '常熟公交线路', type: '公交', route: '覆盖全市，通往各景点', price: '1-2元'}),
               (changshukeyun:Transportation {name: '常熟汽车客运站', type: '大巴', route: '频繁往返上海、苏州、无锡等周边城市'})
           """)

            # 4. 创建关系：景点→城市
            session.run("""
               MATCH (a:Attraction), (c:City {name: '常熟'})
               WHERE a.name IN ['沙家浜·虞山尚湖旅游区', '方塔园']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建关系：城市→推荐美食
            session.run("""
               MATCH (c:City {name: '常熟'}), (f:Food)
               WHERE f.name IN ['叫化鸡', '蕈油面']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建关系：景点→附近美食
            session.run("""
               MATCH (a:Attraction {name: '沙家浜·虞山尚湖旅游区'}), (f:Food {name: '蕈油面'})
               CREATE (a)-[:NEAR_FOOD {distance: '虞山脚下面馆为首选品尝地'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '沙家浜·虞山尚湖旅游区'}), (f:Food {name: '叫化鸡'})
               CREATE (a)-[:NEAR_FOOD {distance: '景区及市区餐馆可体验'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '方塔园'}), (f:Food)
               WHERE f.name IN ['叫化鸡', '蕈油面']
               CREATE (a)-[:NEAR_FOOD {distance: '市区老字号餐馆可找到'}]->(f)
           """)

            # 7. 创建关系：景点→附近住宿
            session.run("""
               MATCH (a:Attraction {name: '沙家浜·虞山尚湖旅游区'}), (ac:Accommodation {name: '常熟阅山轩假日休闲酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '位于虞山脚下，邻近景区'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '方塔园'}), (ac:Accommodation {name: '常熟日航国际酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '市区五星级选择，交通便利'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction), (ac:Accommodation)
               WHERE (a.name = '沙家浜·虞山尚湖旅游区' AND ac.name = '常熟日航国际酒店')
                  OR (a.name = '方塔园' AND ac.name = '常熟阅山轩假日休闲酒店')
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '跨区交通可达，依需求选择'}]->(ac)
           """)

            # 8. 创建关系：城市→交通
            session.run("""
               MATCH (c:City {name: '常熟'}), (t:Transportation)
               WHERE t.name IN ['常熟公交线路', '常熟汽车客运站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)

        print("常熟市旅游数据导入完成！")

    def import_zhangjiagang_data(self):
        """导入张家港市旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (zhangjiagang:City {name: '张家港', level: '县级市（由苏州市代管）', description: '位于江苏省南部，由苏州、无锡、常州三市管辖的沙洲组成而得名，是一座新兴的港口工业城市，荣获全国首个“文明城市”五连冠，被誉为“长江明珠”、“文明之城”'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (xiangshan:Attraction {name: '香山风景区', type: '自然+人文景观', rating: 4.4, opening_hours: '8:00-16:30'}),
               (yonglian:Attraction {name: '永联江南农耕文化园', type: '人文+农业观光', rating: 4.3, opening_hours: '8:30-17:00'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (changjiangsanxian:Food {name: '长江三鲜', type: '地方特色', price_range: '高', description: '指河豚、鲥鱼、刀鱼，肉质鲜美，为时令珍馐'}),
               (tuolubing:Food {name: '张家港拖炉饼', type: '小吃', price_range: '低', description: '油酥香甜，工艺独特，是传统风味点心'}),
               (wanhaozjg:Accommodation {name: '张家港万豪酒店', type: '五星级酒店', price_range: '高', rating: 4.6}),
               (huafangyuan:Accommodation {name: '张家港华芳园国际酒店', type: '商务酒店', price_range: '中', rating: 4.4}),
               (zjggongjiao:Transportation {name: '张家港公交线路', type: '公交', route: '覆盖全市', price: '1-2元'}),
               (zhangjiagangzhan:Transportation {name: '张家港站', type: '高铁', route: '沪苏通铁路、南沿江高铁，连通上海、南京等地'})
           """)

            # 4. 创建关系：景点→城市
            session.run("""
               MATCH (a:Attraction), (c:City {name: '张家港'})
               WHERE a.name IN ['香山风景区', '永联江南农耕文化园']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建关系：城市→推荐美食
            session.run("""
               MATCH (c:City {name: '张家港'}), (f:Food)
               WHERE f.name IN ['长江三鲜', '张家港拖炉饼']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建关系：景点→附近美食
            session.run("""
               MATCH (a:Attraction), (f:Food {name: '长江三鲜'})
               WHERE a.name IN ['香山风景区', '永联江南农耕文化园']
               CREATE (a)-[:NEAR_FOOD {distance: '沿江地区特色餐馆可品尝江鲜'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction), (f:Food {name: '张家港拖炉饼'})
               WHERE a.name IN ['香山风景区', '永联江南农耕文化园']
               CREATE (a)-[:NEAR_FOOD {distance: '景区周边及市区传统点心店有售'}]->(f)
           """)

            # 7. 创建关系：景点→附近住宿
            session.run("""
               MATCH (a:Attraction), (ac:Accommodation)
               WHERE a.name IN ['香山风景区', '永联江南农耕文化园']
                 AND ac.name IN ['张家港万豪酒店', '张家港华芳园国际酒店']
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '建议返回市区住宿'}]->(ac)
           """)

            # 8. 创建关系：城市→交通
            session.run("""
               MATCH (c:City {name: '张家港'}), (t:Transportation)
               WHERE t.name IN ['张家港公交线路', '张家港站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)

        print("张家港市旅游数据导入完成！")

    def import_kunshan_data(self):
        """导入昆山市旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (kunshan:City {name: '昆山', level: '县级市（由苏州市代管）', description: '位于江苏省东南部，是苏州市下辖的县级市，连续多年位居全国百强县市榜首，被誉为“中国最强县”。其昆曲发源地底蕴与现代电子产业并存。'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (zhouzhuang:Attraction {name: '周庄古镇', type: '人文景观', rating: 4.6, opening_hours: '全天开放（内部景点时间不一）'}),
               (tinglinyuan:Attraction {name: '亭林园', type: '自然+人文景观', rating: 4.5, opening_hours: '8:00-16:30'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (aozaomian:Food {name: '奥灶面', type: '小吃', price_range: '低', description: '汤底鲜美，面条劲道，是昆山招牌面食'}),
               (wansantí:Food {name: '万三蹄', type: '地方特色', price_range: '中', description: '源自周庄，色泽酱红，皮润肉酥'}),
               (ruishidajiudian:Accommodation {name: '昆山瑞士大酒店', type: '五星级酒店', price_range: '高', rating: 4.6}),
               (zhouzhuanghuajiantang:Accommodation {name: '周庄花间堂', type: '精品民宿', price_range: '中高', rating: 4.7}),
               (kunshangongjiao:Transportation {name: '昆山公交线路', type: '公交', route: '覆盖全市，连接上海轨道交通11号线', price: '1-4元'}),
               (kunshannanzhan:Transportation {name: '昆山南站', type: '高铁', route: '京沪高铁线，频繁往返上海、苏州、南京'})
           """)

            # 4. 创建关系：景点→城市
            session.run("""
               MATCH (a:Attraction), (c:City {name: '昆山'})
               WHERE a.name IN ['周庄古镇', '亭林园']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建关系：城市→推荐美食
            session.run("""
               MATCH (c:City {name: '昆山'}), (f:Food)
               WHERE f.name IN ['奥灶面', '万三蹄']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建关系：景点→附近美食
            session.run("""
               MATCH (a:Attraction {name: '周庄古镇'}), (f:Food)
               WHERE f.name IN ['奥灶面', '万三蹄']
               CREATE (a)-[:NEAR_FOOD {distance: '古镇内可品尝地道风味'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '亭林园'}), (f:Food {name: '奥灶面'})
               CREATE (a)-[:NEAR_FOOD {distance: '市区老字号面馆可体验'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '亭林园'}), (f:Food {name: '万三蹄'})
               CREATE (a)-[:NEAR_FOOD {distance: '市区特产店及餐馆有售'}]->(f)
           """)

            # 7. 创建关系：景点→附近住宿
            session.run("""
               MATCH (a:Attraction {name: '周庄古镇'}), (ac:Accommodation {name: '周庄花间堂'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '位于古镇内，体验感佳'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '亭林园'}), (ac:Accommodation {name: '昆山瑞士大酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '市区五星级选择，交通便利'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '周庄古镇'}), (ac:Accommodation {name: '昆山瑞士大酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '市区高端选择，需驾车前往景区'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '亭林园'}), (ac:Accommodation {name: '周庄花间堂'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '跨区域民宿选择，适合深度游'}]->(ac)
           """)

            # 8. 创建关系：城市→交通
            session.run("""
               MATCH (c:City {name: '昆山'}), (t:Transportation)
               WHERE t.name IN ['昆山公交线路', '昆山南站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)

        print("昆山市旅游数据导入完成！")

    def import_taicang_data(self):
        """导入太仓市旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (taicang:City {name: '太仓', level: '县级市（由苏州市代管）', description: '位于江苏省东南端，长江口南岸，因春秋时期吴王在此设立粮仓而得名，素有“锦绣江南金太仓”的美誉。作为“德企之乡”，是德国企业在中国的重要集聚地。'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (jincanghu:Attraction {name: '金仓湖公园', type: '自然景观', rating: 4.5, opening_hours: '全天开放'}),
               (shaxiguzhen:Attraction {name: '沙溪古镇', type: '人文景观', rating: 4.4, opening_hours: '全天开放（内部景点时间不一）'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (taicangrousong:Food {name: '太仓肉松', type: '地方特产', price_range: '中', description: '纤维细长，酥松柔软，咸中带甜，闻名全国'}),
               (changjiangjiangxian:Food {name: '长江江鲜', type: '地方特色', price_range: '中高', description: '地处长江入海口，盛产各类时令江鲜，鲜美独特'}),
               (baolongfupeng:Accommodation {name: '太仓宝龙福朋喜来登酒店', type: '商务酒店', price_range: '中高', rating: 4.5}),
               (huafaboman:Accommodation {name: '太仓华发铂尔曼酒店', type: '高端酒店', price_range: '高', rating: 4.6}),
               (taicanggongjiao:Transportation {name: '太仓公交线路', type: '公交', route: '覆盖全市', price: '1-2元'}),
               (taicangzhan:Transportation {name: '太仓站（在建）/太仓南站', type: '高铁', route: '沪苏通铁路，连通上海、南通等地'})
           """)

            # 4. 创建关系：景点→城市
            session.run("""
               MATCH (a:Attraction), (c:City {name: '太仓'})
               WHERE a.name IN ['金仓湖公园', '沙溪古镇']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建关系：城市→推荐美食
            session.run("""
               MATCH (c:City {name: '太仓'}), (f:Food)
               WHERE f.name IN ['太仓肉松', '长江江鲜']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建关系：景点→附近美食
            session.run("""
               MATCH (a:Attraction {name: '沙溪古镇'}), (f:Food)
               WHERE f.name IN ['太仓肉松', '长江江鲜']
               CREATE (a)-[:NEAR_FOOD {distance: '古镇及浏河渔港可品尝'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '金仓湖公园'}), (f:Food {name: '太仓肉松'})
               CREATE (a)-[:NEAR_FOOD {distance: '市区特产店及超市有售'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '金仓湖公园'}), (f:Food {name: '长江江鲜'})
               CREATE (a)-[:NEAR_FOOD {distance: '建议前往浏河渔港品尝新鲜江鲜'}]->(f)
           """)

            # 7. 创建关系：景点→附近住宿
            session.run("""
               MATCH (a:Attraction {name: '金仓湖公园'}), (ac:Accommodation)
               WHERE ac.name IN ['太仓宝龙福朋喜来登酒店', '太仓华发铂尔曼酒店']
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '需返回市区住宿'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '沙溪古镇'}), (ac:Accommodation)
               WHERE ac.name IN ['太仓宝龙福朋喜来登酒店', '太仓华发铂尔曼酒店']
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '市区住宿选择，交通便利'}]->(ac)
           """)

            # 8. 创建关系：城市→交通
            session.run("""
               MATCH (c:City {name: '太仓'}), (t:Transportation)
               WHERE t.name IN ['太仓公交线路', '太仓站（在建）/太仓南站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)

        print("太仓市旅游数据导入完成！")

    def import_qidong_data(self):
        """导入启东市旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (qidong:City {name: '启东', level: '县级市（由南通市代管）', description: '位于江苏省最东端，长江、东海、黄海三水交汇之处，是出江入海的重要门户，被誉为“江海明珠”。因日出最早，又有“江苏第一缕阳光升起之地”的说法。'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (huangjinhaitan:Attraction {name: '黄金海滩', type: '自然景观', rating: 4.3, opening_hours: '8:30-17:00'}),
               (bihaiyinsha:Attraction {name: '启东碧海银沙', type: '人造景观', rating: 4.4, opening_hours: '9:00-17:00'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (qidonghaixian:Food {name: '启东海鲜', type: '地方特色', price_range: '中', description: '吕四渔港是中国四大渔港之一，海鲜种类繁多，新鲜味美'}),
               (qidongmianbing:Food {name: '启东面饼', type: '小吃', price_range: '低', description: '当地特色主食，可卷菜食用，柔软筋道'}),
               (hengdaweinis:Accommodation {name: '启东恒大海上威尼斯酒店', type: '度假酒店', price_range: '高', rating: 4.5}),
               (xidun:Accommodation {name: '启东希尔顿逸林酒店', type: '商务酒店', price_range: '中高', rating: 4.4}),
               (qidonggongjiao:Transportation {name: '启东公交线路', type: '公交', route: '覆盖城区及主要乡镇', price: '1-4元'}),
               (qidongkeyun:Transportation {name: '启东客运站', type: '大巴', route: '频繁往返上海（崇明线）、南通等地'})
           """)

            # 4. 创建关系：景点→城市
            session.run("""
               MATCH (a:Attraction), (c:City {name: '启东'})
               WHERE a.name IN ['黄金海滩', '启东碧海银沙']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建关系：城市→推荐美食
            session.run("""
               MATCH (c:City {name: '启东'}), (f:Food)
               WHERE f.name IN ['启东海鲜', '启东面饼']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建关系：景点→附近美食
            session.run("""
               MATCH (a:Attraction), (f:Food {name: '启东海鲜'})
               WHERE a.name IN ['黄金海滩', '启东碧海银沙']
               CREATE (a)-[:NEAR_FOOD {distance: '吕四港镇为品尝和购买首选地'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction), (f:Food {name: '启东面饼'})
               WHERE a.name IN ['黄金海滩', '启东碧海银沙']
               CREATE (a)-[:NEAR_FOOD {distance: '景区周边餐馆及市区可提供'}]->(f)
           """)

            # 7. 创建关系：景点→附近住宿
            session.run("""
               MATCH (a:Attraction {name: '黄金海滩'}), (ac:Accommodation {name: '启东恒大海上威尼斯酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '毗邻景区，度假体验佳'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '启东碧海银沙'}), (ac:Accommodation {name: '启东恒大海上威尼斯酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '景区配套度假酒店'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction), (ac:Accommodation {name: '启东希尔顿逸林酒店'})
               WHERE a.name IN ['黄金海滩', '启东碧海银沙']
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '市区商务选择，交通可达'}]->(ac)
           """)

            # 8. 创建关系：城市→交通
            session.run("""
               MATCH (c:City {name: '启东'}), (t:Transportation)
               WHERE t.name IN ['启东公交线路', '启东客运站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)

        print("启东市旅游数据导入完成！")

    def import_rugao_data(self):
        """导入如皋市旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (rugao:City {name: '如皋', level: '县级市（由南通市代管）', description: '位于江苏省东部，长江三角洲北翼，是中国著名的“长寿之乡”，历史上被誉为“江苏历史文化名城”。城内水系纵横，拥有独特的水绘园等古典园林。'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (shuihuiyuan:Attraction {name: '水绘园', type: '人文景观', rating: 4.6, opening_hours: '8:00-17:30'}),
               (dongfangdashouxingyuan:Attraction {name: '东方大寿星园', type: '人文景观', rating: 4.3, opening_hours: '8:30-17:00'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (rugaodongtang:Food {name: '如皋董糖', type: '地方特产', price_range: '低', description: '酥松香甜，由明末名妓董小宛创制，历史悠久'}),
               (rugaohuotui:Food {name: '如皋火腿', type: '地方特产', price_range: '中', description: '与金华火腿、宣威火腿齐名，咸香醇厚'}),
               (linzichao糕:Food {name: '林梓潮糕', type: '传统茶食', price_range: '低', description: '糯而不粘，甜而不腻，是当地特色糕点'}),
               (kaiyuanduming:Accommodation {name: '如皋开元名都大酒店', type: '五星级酒店', price_range: '高', rating: 4.5}),
               (zhishuimingren:Accommodation {name: '如皋雉水名人酒店', type: '商务酒店', price_range: '中', rating: 4.3}),
               (rugaogongjiao:Transportation {name: '如皋公交线路', type: '公交', route: '覆盖城区', price: '1-2元'}),
               (rugaonanzhan:Transportation {name: '如皋南站', type: '高铁', route: '盐通高铁线，连通南通、盐城等地'})
           """)

            # 4. 创建关系：景点→城市
            session.run("""
               MATCH (a:Attraction), (c:City {name: '如皋'})
               WHERE a.name IN ['水绘园', '东方大寿星园']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建关系：城市→推荐美食
            session.run("""
               MATCH (c:City {name: '如皋'}), (f:Food)
               WHERE f.name IN ['如皋董糖', '如皋火腿', '林梓潮糕']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建关系：景点→附近美食
            session.run("""
               MATCH (a:Attraction {name: '水绘园'}), (f:Food)
               WHERE f.name IN ['如皋董糖', '如皋火腿', '林梓潮糕']
               CREATE (a)-[:NEAR_FOOD {distance: '附近及东大街历史街区可购买'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '东方大寿星园'}), (f:Food)
               WHERE f.name IN ['如皋董糖', '如皋火腿', '林梓潮糕']
               CREATE (a)-[:NEAR_FOOD {distance: '市区特产店及超市有售'}]->(f)
           """)

            # 7. 创建关系：景点→附近住宿
            session.run("""
               MATCH (a:Attraction {name: '水绘园'}), (ac:Accommodation {name: '如皋雉水名人酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '约1.5km'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '水绘园'}), (ac:Accommodation {name: '如皋开元名都大酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '市区五星级选择，交通便利'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '东方大寿星园'}), (ac:Accommodation)
               WHERE ac.name IN ['如皋开元名都大酒店', '如皋雉水名人酒店']
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '市区住宿，交通可达'}]->(ac)
           """)

            # 8. 创建关系：城市→交通
            session.run("""
               MATCH (c:City {name: '如皋'}), (t:Transportation)
               WHERE t.name IN ['如皋公交线路', '如皋南站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)

        print("如皋市旅游数据导入完成！")

    def import_haian_data(self):
        """导入海安市旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (haian:City {name: '海安', level: '县级市（由南通市代管）', description: '位于江苏省东部，地处南通、盐城、泰州三市交界处，是苏中水陆交通要冲，被誉为“苏中水陆门户”。因“海水不扬波”之意而得名，是江海文明的起源地之一。'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (jianghuaiwenhuayuan:Attraction {name: '江淮文化园', type: '人文景观', rating: 4.4, opening_hours: '8:30-17:00'}),
               (qixinghushengtaiyuan:Attraction {name: '七星湖生态园', type: '自然景观', rating: 4.3, opening_hours: '全天开放'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (maxiajang:Food {name: '麻虾酱', type: '地方特产', price_range: '中低', description: '用淡水小麻虾制成，鲜美无比，是下饭佐粥的佳品'}),
               (haitunyu_haian:Food {name: '河豚鱼', type: '地方特色', price_range: '中高', description: '烹制技艺成熟，肉质细腻，鲜美绝伦'}),
               (libaibaiye:Food {name: '李堡百叶', type: '豆制品', price_range: '低', description: '豆香浓郁，口感筋道，是当地特色食材'}),
               (jinzhuanjiudian:Accommodation {name: '海安金砖酒店', type: '五星级酒店', price_range: '高', rating: 4.6}),
               (wangfubangrui:Accommodation {name: '海安王府邦瑞国际大酒店', type: '商务酒店', price_range: '中', rating: 4.4}),
               (haiangongjiao:Transportation {name: '海安公交线路', type: '公交', route: '覆盖城区', price: '1-2元'}),
               (haianzhan:Transportation {name: '海安站', type: '高铁', route: '新长铁路、盐通高铁，枢纽地位重要'})
           """)

            # 4. 创建关系：景点→城市
            session.run("""
               MATCH (a:Attraction), (c:City {name: '海安'})
               WHERE a.name IN ['江淮文化园', '七星湖生态园']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建关系：城市→推荐美食
            session.run("""
               MATCH (c:City {name: '海安'}), (f:Food)
               WHERE f.name IN ['麻虾酱', '河豚鱼', '李堡百叶']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建关系：景点→附近美食
            session.run("""
               MATCH (a:Attraction), (f:Food)
               WHERE a.name IN ['江淮文化园', '七星湖生态园']
                 AND f.name IN ['麻虾酱', '河豚鱼']
               CREATE (a)-[:NEAR_FOOD {distance: '老坝港等沿河地区可品尝购买'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction), (f:Food {name: '李堡百叶'})
               WHERE a.name IN ['江淮文化园', '七星湖生态园']
               CREATE (a)-[:NEAR_FOOD {distance: '市区农贸市场及餐馆可找到'}]->(f)
           """)

            # 7. 创建关系：景点→附近住宿
            session.run("""
               MATCH (a:Attraction {name: '七星湖生态园'}), (ac:Accommodation {name: '海安金砖酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '位于园区旁，景观优越'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '江淮文化园'}), (ac:Accommodation)
               WHERE ac.name IN ['海安金砖酒店', '海安王府邦瑞国际大酒店']
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '市区住宿选择，交通便捷'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '七星湖生态园'}), (ac:Accommodation {name: '海安王府邦瑞国际大酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '市区商务选择，交通可达'}]->(ac)
           """)

            # 8. 创建关系：城市→交通
            session.run("""
               MATCH (c:City {name: '海安'}), (t:Transportation)
               WHERE t.name IN ['海安公交线路', '海安站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)

        print("海安市旅游数据导入完成！")

    def import_dongtai_data(self):
        """导入东台市旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (dongtai:City {name: '东台', level: '县级市（由盐城市代管）', description: '位于江苏省中部，盐城市最南端，是里下河地区典型的“鱼米之乡”。这里拥有中国首个滨海湿地类世界自然遗产——中国黄（渤）海候鸟栖息地，被誉为“黄海明珠”。'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (huanghaisenlin:Attraction {name: '黄海森林公园', type: '自然景观', rating: 4.7, opening_hours: '8:30-17:30'}),
               (xixijq:Attraction {name: '西溪旅游文化景区', type: '人文+自然景观', rating: 4.5, opening_hours: '全天开放（内部景点时间不一）'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (yutangmian:Food {name: '东台鱼汤面', type: '地方特色', price_range: '低', description: '汤色乳白，醇厚鲜美，面条筋道，是早茶经典'}),
               (chenpijiu:Food {name: '陈皮酒', type: '地方特产', price_range: '中低', description: '传统药酒，香甜醇厚，有养生功效'}),
               (suerbing:Food {name: '酥儿饼', type: '传统茶食', price_range: '低', description: '层层酥脆，内馅香甜，是当地特色糕点'}),
               (senlinwenquan:Accommodation {name: '东台黄海森林温泉酒店', type: '度假酒店', price_range: '中高', rating: 4.6}),
               (guojidajiudian:Accommodation {name: '东台国际大酒店', type: '商务酒店', price_range: '中', rating: 4.4}),
               (dongtaigongjiao:Transportation {name: '东台公交线路', type: '公交', route: '覆盖城区及主要景点', price: '1-3元'}),
               (dongtaizhan:Transportation {name: '东台站', type: '高铁', route: '盐通高铁线，连通盐城、南通等地'})
           """)

            # 4. 创建关系：景点→城市
            session.run("""
               MATCH (a:Attraction), (c:City {name: '东台'})
               WHERE a.name IN ['黄海森林公园', '西溪旅游文化景区']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建关系：城市→推荐美食
            session.run("""
               MATCH (c:City {name: '东台'}), (f:Food)
               WHERE f.name IN ['东台鱼汤面', '陈皮酒', '酥儿饼']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建关系：景点→附近美食
            session.run("""
               MATCH (a:Attraction {name: '西溪旅游文化景区'}), (f:Food)
               WHERE f.name IN ['东台鱼汤面', '陈皮酒', '酥儿饼']
               CREATE (a)-[:NEAR_FOOD {distance: '景区内草市街及市区早茶店可品尝'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '黄海森林公园'}), (f:Food {name: '东台鱼汤面'})
               CREATE (a)-[:NEAR_FOOD {distance: '建议返回市区品尝正宗风味'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '黄海森林公园'}), (f:Food)
               WHERE f.name IN ['陈皮酒', '酥儿饼']
               CREATE (a)-[:NEAR_FOOD {distance: '景区服务区及市区特产店有售'}]->(f)
           """)

            # 7. 创建关系：景点→附近住宿
            session.run("""
               MATCH (a:Attraction {name: '黄海森林公园'}), (ac:Accommodation {name: '东台黄海森林温泉酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '位于公园内，度假体验佳'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '西溪旅游文化景区'}), (ac:Accommodation)
               WHERE ac.name IN ['东台国际大酒店', '东台黄海森林温泉酒店']
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '市区住宿选择，交通便利'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '黄海森林公园'}), (ac:Accommodation {name: '东台国际大酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '市区商务选择，需驾车前往'}]->(ac)
           """)

            # 8. 创建关系：城市→交通
            session.run("""
               MATCH (c:City {name: '东台'}), (t:Transportation)
               WHERE t.name IN ['东台公交线路', '东台站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)

        print("东台市旅游数据导入完成！")

    def import_yizheng_data(self):
        """导入仪征市旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (yizheng:City {name: '仪征', level: '县级市（由扬州市代管）', description: '位于江苏省中西部，长江下游北岸，是宁镇扬同城化中心地带。历史上因宋真宗在此铸造皇家祭祀器物而得名，是“风物淮南第一州”，也是中国重要的化纤和汽车工业基地。'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (nashandizhi:Attraction {name: '捺山地质公园', type: '自然景观', rating: 4.5, opening_hours: '8:30-17:00'}),
               (tianlehu:Attraction {name: '天乐湖旅游度假区', type: '自然+娱乐景观', rating: 4.3, opening_hours: '9:00-17:00'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (yizhengzicai:Food {name: '仪征紫菜', type: '地方特产', price_range: '低', description: '沿江地区特产，口感细嫩，味道鲜美'}),
               (dayifenge:Food {name: '大仪风鹅', type: '地方特产', price_range: '中', description: '肉质紧密，酥香可口，是当地名产'}),
               (shierweichagan:Food {name: '十二圩茶干', type: '豆制品', price_range: '低', description: '五香风味，口感紧实，是佐餐佳品'}),
               (dongyuanfandian:Accommodation {name: '仪征东园饭店', type: '商务酒店', price_range: '中', rating: 4.3}),
               (natianminsu:Accommodation {name: '捺山那田民宿', type: '特色民宿', price_range: '中', rating: 4.5}),
               (yizhenggongjiao:Transportation {name: '仪征公交线路', type: '公交', route: '覆盖城区，连接扬州', price: '1-3元'}),
               (yizhengkeyun:Transportation {name: '仪征客运枢纽', type: '大巴/公交', route: '频繁往返南京、扬州'})
           """)

            # 4. 创建关系：景点→城市
            session.run("""
               MATCH (a:Attraction), (c:City {name: '仪征'})
               WHERE a.name IN ['捺山地质公园', '天乐湖旅游度假区']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建关系：城市→推荐美食
            session.run("""
               MATCH (c:City {name: '仪征'}), (f:Food)
               WHERE f.name IN ['仪征紫菜', '大仪风鹅', '十二圩茶干']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建关系：景点→附近美食
            session.run("""
               MATCH (a:Attraction), (f:Food {name: '十二圩茶干'})
               WHERE a.name IN ['捺山地质公园', '天乐湖旅游度假区']
               CREATE (a)-[:NEAR_FOOD {distance: '十二圩街道为购买首选地'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction), (f:Food {name: '大仪风鹅'})
               WHERE a.name IN ['捺山地质公园', '天乐湖旅游度假区']
               CREATE (a)-[:NEAR_FOOD {distance: '市区特产店及大仪镇可购买'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction), (f:Food {name: '仪征紫菜'})
               WHERE a.name IN ['捺山地质公园', '天乐湖旅游度假区']
               CREATE (a)-[:NEAR_FOOD {distance: '沿江市场及市区商超有售'}]->(f)
           """)

            # 7. 创建关系：景点→附近住宿
            session.run("""
               MATCH (a:Attraction {name: '捺山地质公园'}), (ac:Accommodation {name: '捺山那田民宿'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '位于景区旁，特色体验佳'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '天乐湖旅游度假区'}), (ac:Accommodation {name: '仪征东园饭店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '市区商务选择，交通可达'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '天乐湖旅游度假区'}), (ac:Accommodation {name: '捺山那田民宿'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '跨景区特色住宿，适合深度游'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '捺山地质公园'}), (ac:Accommodation {name: '仪征东园饭店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '市区住宿选择，交通便利'}]->(ac)
           """)

            # 8. 创建关系：城市→交通
            session.run("""
               MATCH (c:City {name: '仪征'}), (t:Transportation)
               WHERE t.name IN ['仪征公交线路', '仪征客运枢纽']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)

        print("仪征市旅游数据导入完成！")

    def import_gaoyou_data(self):
        """导入高邮市旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (gaoyou:City {name: '高邮', level: '县级市（由扬州市代管）', description: '位于江苏省中部，淮河下游，是中国唯一以“邮”命名的城市，被誉为“中华邮城”。同时拥有秀丽的高邮湖，是著名的“鱼米之乡”。'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (yuchengyi:Attraction {name: '盂城驿', type: '人文景观', rating: 4.5, opening_hours: '8:30-17:30'}),
               (gaoyouhu:Attraction {name: '高邮湖', type: '自然景观', rating: 4.4, opening_hours: '全天开放'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (xiandanyake:Food {name: '高邮咸鸭蛋', type: '地方特产', price_range: '低', description: '蛋白鲜嫩，蛋黄红润流油，享誉全国'}),
               (dazhaxie:Food {name: '高邮湖大闸蟹', type: '地方特色', price_range: '中', description: '膏肥黄满，肉质鲜甜，不输阳澄湖'}),
               (qinyoudongtang:Food {name: '秦邮董糖', type: '传统茶食', price_range: '低', description: '与如皋董糖同源，酥松香甜'}),
               (huijinjilin:Accommodation {name: '高邮汇金金陵大饭店', type: '五星级酒店', price_range: '高', rating: 4.5}),
               (bosideng:Accommodation {name: '高邮波司登国际大酒店', type: '商务酒店', price_range: '中', rating: 4.3}),
               (gaoyougongjiao:Transportation {name: '高邮公交线路', type: '公交', route: '覆盖城区', price: '1-2元'}),
               (gaoyouzhan:Transportation {name: '高邮站/高邮北站', type: '高铁', route: '连镇高铁线，连通扬州、淮安等地'})
           """)

            # 4. 创建关系：景点→城市
            session.run("""
               MATCH (a:Attraction), (c:City {name: '高邮'})
               WHERE a.name IN ['盂城驿', '高邮湖']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建关系：城市→推荐美食
            session.run("""
               MATCH (c:City {name: '高邮'}), (f:Food)
               WHERE f.name IN ['高邮咸鸭蛋', '高邮湖大闸蟹', '秦邮董糖']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建关系：景点→附近美食
            session.run("""
               MATCH (a:Attraction), (f:Food)
               WHERE a.name IN ['盂城驿', '高邮湖']
                 AND f.name IN ['高邮咸鸭蛋', '高邮湖大闸蟹']
               CREATE (a)-[:NEAR_FOOD {distance: '湖周边及景区可品尝购买'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '盂城驿'}), (f:Food {name: '秦邮董糖'})
               CREATE (a)-[:NEAR_FOOD {distance: '景区周边特产店有售'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '高邮湖'}), (f:Food {name: '秦邮董糖'})
               CREATE (a)-[:NEAR_FOOD {distance: '建议前往市区购买正宗产品'}]->(f)
           """)

            # 7. 创建关系：景点→附近住宿
            session.run("""
               MATCH (a:Attraction {name: '盂城驿'}), (ac:Accommodation {name: '高邮汇金金陵大饭店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '位于市区，交通便利'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '盂城驿'}), (ac:Accommodation {name: '高邮波司登国际大酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '市区商务选择，便捷可达'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '高邮湖'}), (ac:Accommodation)
               WHERE ac.name IN ['高邮汇金金陵大饭店', '高邮波司登国际大酒店']
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '市区住宿，驾车前往湖区'}]->(ac)
           """)

            # 8. 创建关系：城市→交通
            session.run("""
               MATCH (c:City {name: '高邮'}), (t:Transportation)
               WHERE t.name IN ['高邮公交线路', '高邮站/高邮北站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)

        print("高邮市旅游数据导入完成！")

    def import_danyang_data(self):
        """导入丹阳市旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (danyang:City {name: '丹阳', level: '县级市（由镇江市代管）', description: '位于江苏省南部，是江苏省南部重要的交通枢纽和商品集散地。丹阳以“眼镜之都”闻名全国，同时也是吴文化的发源地之一，存有南朝陵墓石刻等珍贵文物。'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (yanjingcheng:Attraction {name: '丹阳眼镜城', type: '特色商业', rating: 4.3, opening_hours: '9:00-17:30'}),
               (shikepark:Attraction {name: '天地石刻园', type: '人文景观', rating: 4.2, opening_hours: '9:00-17:00'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (damizhou:Food {name: '丹阳大麦粥', type: '地方特色', price_range: '低', description: '用大麦仁熬制，米香浓郁，爽滑暖胃'}),
               (yanlingyajiao:Food {name: '延陵鸭饺', type: '小吃', price_range: '中低', description: '鸭肉馅的馄饨，汤鲜味美，肉质紧实'}),
               (jiepaidoufu:Food {name: '界牌豆腐', type: '豆制品', price_range: '低', description: '口感嫩滑，豆香纯正，是当地特色食材'}),
               (shuizhongxian:Accommodation {name: '丹阳水中仙国际酒店', type: '高端酒店', price_range: '中高', rating: 4.4}),
               (jinying:Accommodation {name: '丹阳金鹰国际酒店', type: '商务酒店', price_range: '中', rating: 4.3}),
               (danyanggongjiao:Transportation {name: '丹阳公交线路', type: '公交', route: '覆盖城区及眼镜城', price: '1-2元'}),
               (danyangzhan:Transportation {name: '丹阳站/丹阳北站', type: '高铁', route: '京沪高铁、沪宁城际，枢纽地位重要'})
           """)

            # 4. 创建关系：景点→城市
            session.run("""
               MATCH (a:Attraction), (c:City {name: '丹阳'})
               WHERE a.name IN ['丹阳眼镜城', '天地石刻园']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建关系：城市→推荐美食
            session.run("""
               MATCH (c:City {name: '丹阳'}), (f:Food)
               WHERE f.name IN ['丹阳大麦粥', '延陵鸭饺', '界牌豆腐']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建关系：景点→附近美食
            session.run("""
               MATCH (a:Attraction), (f:Food)
               WHERE a.name IN ['丹阳眼镜城', '天地石刻园']
                 AND f.name IN ['丹阳大麦粥', '延陵鸭饺']
               CREATE (a)-[:NEAR_FOOD {distance: '市区早餐店及面馆可品尝'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction), (f:Food {name: '界牌豆腐'})
               WHERE a.name IN ['丹阳眼镜城', '天地石刻园']
               CREATE (a)-[:NEAR_FOOD {distance: '界牌镇及市区餐馆可找到'}]->(f)
           """)

            # 7. 创建关系：景点→附近住宿
            session.run("""
               MATCH (a:Attraction {name: '丹阳眼镜城'}), (ac:Accommodation {name: '丹阳水中仙国际酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '位于市中心，邻近眼镜城'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '丹阳眼镜城'}), (ac:Accommodation {name: '丹阳金鹰国际酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '市区商务选择，交通便捷'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '天地石刻园'}), (ac:Accommodation)
               WHERE ac.name IN ['丹阳水中仙国际酒店', '丹阳金鹰国际酒店']
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '市区住宿，驾车前往景区'}]->(ac)
           """)

            # 8. 创建关系：城市→交通
            session.run("""
               MATCH (c:City {name: '丹阳'}), (t:Transportation)
               WHERE t.name IN ['丹阳公交线路', '丹阳站/丹阳北站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)

        print("丹阳市旅游数据导入完成！")

    def import_yangzhong_data(self):
        """导入扬中市旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (yangzhong:City {name: '扬中', level: '县级市（由镇江市代管）', description: '位于江苏省中部，是万里长江中的一座岛市，由雷公岛、太平洲、西沙、中心沙四个江岛组成，素有“河豚之乡”、“江中明珠”的美誉。'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (yuanboyuan:Attraction {name: '园博园', type: '自然+人文景观', rating: 4.3, opening_hours: '8:30-17:00'}),
               (changjiangyuwenhua:Attraction {name: '长江渔文化生态园', type: '自然+文化景观', rating: 4.2, opening_hours: '9:00-17:00'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (hetun_yangzhong:Food {name: '河豚', type: '地方特色', price_range: '中高', description: '扬中是“中国河豚之乡”，烹饪技艺安全精湛，肉质鲜美无比'}),
               (daoyu:Food {name: '刀鱼', type: '地方特色', price_range: '高', description: '春季时令江鲜，肉质细嫩，腴而不腻'}),
               (yangcao:Food {name: '秧草', type: '地方蔬菜', price_range: '低', description: '江岛特色蔬菜，清新解腻，常与河豚、河鳗同烧'}),
               (feiersijinling:Accommodation {name: '扬中菲尔斯金陵大酒店', type: '五星级酒店', price_range: '高', rating: 4.5}),
               (juntaiweijing:Accommodation {name: '扬中君泰维景国际酒店', type: '商务酒店', price_range: '中', rating: 4.3}),
               (yangzhonggongjiao:Transportation {name: '扬中公交线路', type: '公交', route: '环岛及连接市区', price: '1-2元'}),
               (yangzhongdaqiao:Transportation {name: '扬中长江大桥/扬中三桥', type: '公路', route: '连接镇江市区、常州、泰州等地'})
           """)

            # 4. 创建关系：景点→城市
            session.run("""
               MATCH (a:Attraction), (c:City {name: '扬中'})
               WHERE a.name IN ['园博园', '长江渔文化生态园']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建关系：城市→推荐美食
            session.run("""
               MATCH (c:City {name: '扬中'}), (f:Food)
               WHERE f.name IN ['河豚', '刀鱼', '秧草']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建关系：景点→附近美食
            session.run("""
               MATCH (a:Attraction), (f:Food)
               WHERE a.name IN ['园博园', '长江渔文化生态园']
                 AND f.name IN ['河豚', '刀鱼', '秧草']
               CREATE (a)-[:NEAR_FOOD {distance: '新坝镇等地有专营河豚的特色餐馆'}]->(f)
           """)

            # 7. 创建关系：景点→附近住宿
            session.run("""
               MATCH (a:Attraction {name: '园博园'}), (ac:Accommodation {name: '扬中菲尔斯金陵大酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '位于市区，交通便利'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction), (ac:Accommodation {name: '扬中君泰维景国际酒店'})
               WHERE a.name IN ['园博园', '长江渔文化生态园']
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '市区商务选择，便捷可达'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '长江渔文化生态园'}), (ac:Accommodation {name: '扬中菲尔斯金陵大酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '市区五星级选择，驾车前往景区'}]->(ac)
           """)

            # 8. 创建关系：城市→交通
            session.run("""
               MATCH (c:City {name: '扬中'}), (t:Transportation)
               WHERE t.name IN ['扬中公交线路', '扬中长江大桥/扬中三桥']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)

        print("扬中市旅游数据导入完成！")

    def import_jurong_data(self):
        """导入句容市旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (jurong:City {name: '句容', level: '县级市（由镇江市代管）', description: '位于江苏省南部，地处苏南，东连镇江，西接南京，是南京的东南门户，素有“南京新东郊、金陵御花园”之称。境内的道教圣地茅山闻名遐迩。'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (maoshan:Attraction {name: '茅山风景区', type: '自然+人文景观', rating: 4.6, opening_hours: '7:30-17:00'}),
               (baohuashan:Attraction {name: '宝华山国家森林公园', type: '自然+人文景观', rating: 4.5, opening_hours: '8:00-17:00'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (maoshanlaoe:Food {name: '茅山老鹅', type: '地方特产', price_range: '中', description: '选用当地草鹅腌制，肉质紧密，醇香可口'}),
               (dingzhuangputao:Food {name: '丁庄葡萄', type: '地方特产', price_range: '中低', description: '果肉饱满，汁多味甜，是国家地理标志产品'}),
               (gegencha:Food {name: '葛根茶', type: '地方特产', price_range: '低', description: '茅山地区盛产葛根，制成的茶饮有独特风味'}),
               (yukunkaiyuan:Accommodation {name: '句容余坤开元大酒店', type: '高端酒店', price_range: '中高', rating: 4.5}),
               (maoshanwenquan:Accommodation {name: '茅山温泉假日度假酒店', type: '度假酒店', price_range: '中高', rating: 4.4}),
               (juronggongjiao:Transportation {name: '句容公交线路', type: '公交', route: '覆盖城区及连接南京', price: '1-4元'}),
               (jurongxizhan:Transportation {name: '句容西站', type: '高铁', route: '宁杭高铁线，连通南京、杭州'})
           """)

            # 4. 创建关系：景点→城市
            session.run("""
               MATCH (a:Attraction), (c:City {name: '句容'})
               WHERE a.name IN ['茅山风景区', '宝华山国家森林公园']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建关系：城市→推荐美食
            session.run("""
               MATCH (c:City {name: '句容'}), (f:Food)
               WHERE f.name IN ['茅山老鹅', '丁庄葡萄', '葛根茶']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建关系：景点→附近美食
            session.run("""
               MATCH (a:Attraction {name: '茅山风景区'}), (f:Food)
               WHERE f.name IN ['茅山老鹅', '丁庄葡萄', '葛根茶']
               CREATE (a)-[:NEAR_FOOD {distance: '景区周边及天王镇可品尝购买'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '宝华山国家森林公园'}), (f:Food {name: '茅山老鹅'})
               CREATE (a)-[:NEAR_FOOD {distance: '市区及茅山周边可购买'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '宝华山国家森林公园'}), (f:Food)
               WHERE f.name IN ['丁庄葡萄', '葛根茶']
               CREATE (a)-[:NEAR_FOOD {distance: '建议前往丁庄镇及茅山地区购买'}]->(f)
           """)

            # 7. 创建关系：景点→附近住宿
            session.run("""
               MATCH (a:Attraction {name: '茅山风景区'}), (ac:Accommodation {name: '茅山温泉假日度假酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '位于景区附近，度假体验佳'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '茅山风景区'}), (ac:Accommodation {name: '句容余坤开元大酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '市区高端选择，驾车前往景区'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '宝华山国家森林公园'}), (ac:Accommodation)
               WHERE ac.name IN ['句容余坤开元大酒店', '茅山温泉假日度假酒店']
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '跨景区住宿选择，依行程安排'}]->(ac)
           """)

            # 8. 创建关系：城市→交通
            session.run("""
               MATCH (c:City {name: '句容'}), (t:Transportation)
               WHERE t.name IN ['句容公交线路', '句容西站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)

        print("句容市旅游数据导入完成！")

    def import_xinyi_data(self):
        """导入新沂市旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (xy:City {name: '新沂市', level: '县级市（由徐州市代管）', description: '位于江苏省北部，是苏北重要的交通枢纽，被誉为“江苏北大门”、“东陇海线上第三大城市”，历史悠久，素有“钟吾国”之称'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (maling:Attraction {name: '马陵山风景名胜区', type: '自然景观', rating: 4.5, opening_hours: '8:30-17:00'}),
               (yaowan:Attraction {name: '窑湾古镇', type: '人文景观', rating: 4.4, opening_hours: '全天开放（内部景点时间不一）'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (chuancai:Food {name: '窑湾船菜', type: '地方特色', price_range: '中', description: '源自京杭大运河船家，以湖鲜为主，做法独特'}),
               (kunxiangti:Food {name: '新沂捆香蹄', type: '地方特产', price_range: '中', description: '皮脆肉香，口感紧实，是佐餐佳品'}),
               (manhadun:Accommodation {name: '新沂曼哈顿国际酒店', type: '商务酒店', price_range: '中', rating: 4.3}),
               (yaowanminsu:Accommodation {name: '窑湾古镇民宿', type: '特色住宿', price_range: '中低', rating: 4.5}),
               (gongjiao:Transportation {name: '新沂公交线路', type: '公交', route: '覆盖城区', price: '1-2元'}),
               (huochezhan:Transportation {name: '新沂站/新沂南站', type: '铁路', route: '陇海线、徐连高铁，连通徐州、连云港等地', price: '按里程计算'})
           """)

            # 4. 创建关系：景点→城市
            session.run("""
               MATCH (a:Attraction), (c:City {name: '新沂市'})
               WHERE a.name IN ['马陵山风景名胜区', '窑湾古镇']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建关系：城市→推荐美食
            session.run("""
               MATCH (c:City {name: '新沂市'}), (f:Food)
               WHERE f.name IN ['窑湾船菜', '新沂捆香蹄']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建关系：景点→附近美食
            session.run("""
               MATCH (a:Attraction {name: '窑湾古镇'}), (f:Food)
               WHERE f.name IN ['窑湾船菜', '新沂捆香蹄']
               CREATE (a)-[:NEAR_FOOD {distance: '0.5km', description: '可品尝最地道风味'}]->(f)
           """)

            # 7. 创建关系：景点→附近住宿
            session.run("""
               MATCH (a:Attraction {name: '马陵山风景名胜区'}), (ac:Accommodation {name: '新沂曼哈顿国际酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '约15km', description: '需返回市区'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '窑湾古镇'}), (ac:Accommodation {name: '窑湾古镇民宿'})
               CREATE (a)-[:NEAR_FOOD {distance: '0.3km'}]->(ac)
           """)

            # 8. 创建关系：城市→交通
            session.run("""
               MATCH (c:City {name: '新沂市'}), (t:Transportation)
               WHERE t.name IN ['新沂公交线路', '新沂站/新沂南站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)

        print("新沂市旅游数据导入完成！")

    def import_pizhou_data(self):
        """导入邳州市旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (pz:City {name: '邳州市', level: '县级市（由徐州市代管）', description: '位于江苏省北部，是江苏文明最早的起源之一，以“邳”名国，历史悠久。现代是著名的“中国银杏之乡”和“中国板材之乡”'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (aishan:Attraction {name: '艾山九龙风景区', type: '自然+人文景观', rating: 4.4, opening_hours: '8:00-17:00'}),
               (yinxing:Attraction {name: '邳州银杏博览园', type: '自然+农业观光', rating: 4.5, opening_hours: '全天开放（最佳观赏期秋季）'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (pzyx:Food {name: '邳州银杏', type: '地方特产', price_range: '中低', description: '糯软香甜，可盐焗、可入菜，营养丰富'}),
               (pzlt:Food {name: '邳州辣汤', type: '小吃', price_range: '低', description: '胡椒风味浓郁，配料丰富，暖胃驱寒'}),
               (yaduo:Accommodation {name: '邳州宏通客运站亚朵酒店', type: '精品酒店', price_range: '中', rating: 4.5}),
               (xiyue:Accommodation {name: '邳州玺悦国际大酒店', type: '商务酒店', price_range: '中', rating: 4.3}),
               (pzgj:Transportation {name: '邳州公交线路', type: '公交', route: '覆盖城区', price: '1-2元'}),
               (pzdong:Transportation {name: '邳州东站', type: '高铁', route: '徐连高铁线，连通徐州、连云港等地', price: '按里程计算'})
           """)

            # 4. 创建关系：景点→城市
            session.run("""
               MATCH (a:Attraction), (c:City {name: '邳州市'})
               WHERE a.name IN ['艾山九龙风景区', '邳州银杏博览园']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建关系：城市→推荐美食
            session.run("""
               MATCH (c:City {name: '邳州市'}), (f:Food)
               WHERE f.name IN ['邳州银杏', '邳州辣汤']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建关系：景点→附近美食
            session.run("""
               MATCH (a:Attraction {name: '邳州银杏博览园'}), (f:Food {name: '邳州银杏'})
               CREATE (a)-[:NEAR_FOOD {distance: '0.8km', description: '可购买和品尝银杏制品'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '艾山九龙风景区'}), (f:Food {name: '邳州辣汤'})
               CREATE (a)-[:NEAR_FOOD {distance: '约10km', description: '景区周边餐馆可品尝'}]->(f)
           """)

            # 7. 创建关系：景点→附近住宿
            session.run("""
               MATCH (a:Attraction {name: '艾山九龙风景区'}), (ac:Accommodation)
               WHERE ac.name IN ['邳州宏通客运站亚朵酒店', '邳州玺悦国际大酒店']
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '约20km', description: '需返回市区'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '邳州银杏博览园'}), (ac:Accommodation {name: '邳州宏通客运站亚朵酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '约12km'}]->(ac)
           """)

            # 8. 创建关系：城市→交通
            session.run("""
               MATCH (c:City {name: '邳州市'}), (t:Transportation)
               WHERE t.name IN ['邳州公交线路', '邳州东站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)

        print("邳州市旅游数据导入完成！")

    def import_xinghua_data(self):
        """导入兴化市旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (xh:City {name: '兴化市', level: '县级市（由泰州市代管）', description: '位于江苏省中部，长江三角洲北翼，是著名的“鱼米之乡”，国家生态示范区，以其全球重要的农业文化遗产——“垛田”地貌和千岛菜花景观闻名于世，被誉为“中国最美油菜花海”'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (qianduo:Attraction {name: '千垛景区（油菜花田）', type: '自然+农业景观', rating: 4.6, opening_hours: '8:00-17:00'}),
               (lizhong:Attraction {name: '李中水上森林', type: '自然景观', rating: 4.5, opening_hours: '8:30-17:00'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (dazhaxie:Food {name: '兴化大闸蟹', type: '地方特产', price_range: '中', description: '膏脂丰满，肉质鲜甜，是“中国河蟹养殖第一县”'}),
               (shagouyuanyuan:Food {name: '沙沟鱼圆', type: '地方特色', price_range: '中低', description: '口感细腻爽滑，富有弹性，鱼鲜味十足'}),
               (longxiangyu:Food {name: '龙香芋', type: '地方特产', price_range: '低', description: '垛田特产，口感香糯，常用于红烧肉等菜肴'}),
               (tianbao:Accommodation {name: '兴化天宝花园大酒店', type: '商务酒店', price_range: '中', rating: 4.4}),
               (qingfeng:Accommodation {name: '兴化清风精选酒店', type: '精品酒店', price_range: '中', rating: 4.5}),
               (xhgongjiao:Transportation {name: '兴化公交线路', type: '公交', route: '覆盖城区及主要乡镇', price: '1-3元'}),
               (xhkeyunzhan:Transportation {name: '兴化客运站', type: '大巴', route: '连通泰州、扬州、盐城等地', price: '按里程计算'})
           """)

            # 4. 创建关系：景点→城市
            session.run("""
               MATCH (a:Attraction), (c:City {name: '兴化市'})
               WHERE a.name IN ['千垛景区（油菜花田）', '李中水上森林']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建关系：城市→推荐美食
            session.run("""
               MATCH (c:City {name: '兴化市'}), (f:Food)
               WHERE f.name IN ['兴化大闸蟹', '沙沟鱼圆', '龙香芋']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建关系：景点→附近美食
            session.run("""
               MATCH (a:Attraction {name: '千垛景区（油菜花田）'}), (f:Food)
               WHERE f.name IN ['兴化大闸蟹', '龙香芋']
               CREATE (a)-[:NEAR_FOOD {distance: '约5km', description: '景区附近可品尝地道水产'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '千垛景区（油菜花田）'}), (f:Food {name: '沙沟鱼圆'})
               CREATE (a)-[:NEAR_FOOD {distance: '约15km', description: '沙沟镇可品尝正宗风味'}]->(f)
           """)

            # 7. 创建关系：景点→附近住宿
            session.run("""
               MATCH (a:Attraction {name: '千垛景区（油菜花田）'}), (ac:Accommodation)
               WHERE ac.name IN ['兴化天宝花园大酒店', '兴化清风精选酒店']
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '约20km', description: '需返回市区或选择周边民宿'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '李中水上森林'}), (ac:Accommodation {name: '兴化清风精选酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '约18km'}]->(ac)
           """)

            # 8. 创建关系：城市→交通
            session.run("""
               MATCH (c:City {name: '兴化市'}), (t:Transportation)
               WHERE t.name IN ['兴化公交线路', '兴化客运站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)

        print("兴化市旅游数据导入完成！")

    def import_jingjiang_data(self):
        """导入靖江市旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (jj:City {name: '靖江市', level: '县级市（由泰州市代管）', description: '位于江苏省中南部，长江下游北岸，处于长江三角洲苏南苏中连接点，是少有的江北吴语城市。经济发达，被誉为“中国汤包之乡”、“中国山水盆景之城”'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (gushan:Attraction {name: '孤山风景区', type: '自然+人文景观', rating: 4.2, opening_hours: '8:00-16:30'}),
               (mucheng:Attraction {name: '牧城公园', type: '自然景观', rating: 4.4, opening_hours: '全天开放'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (tangbao:Food {name: '靖江蟹黄汤包', type: '地方特色', price_range: '中高', description: '皮薄如纸，汤色金黄，蟹香浓郁，被誉为“中华第一包”'}),
               (jiangxian:Food {name: '长江江鲜', type: '地方特色', price_range: '中高', description: '肉质鲜嫩，种类丰富，包括鲥鱼、刀鱼、河豚等'}),
               (zhuroufu:Food {name: '猪肉脯', type: '地方特产', price_range: '中', description: '色泽棕红，香甜可口，是知名休闲食品'}),
               (jinyue:Accommodation {name: '靖江金悦国际酒店', type: '五星级酒店', price_range: '高', rating: 4.6}),
               (yangzijiang:Accommodation {name: '靖江扬子江大酒店', type: '商务酒店', price_range: '中', rating: 4.3}),
               (jjgongjiao:Transportation {name: '靖江公交线路', type: '公交', route: '覆盖城区', price: '1-2元'}),
               (jiaotong:Transportation {name: '江阴长江大桥/靖江汽渡', type: '公路/轮渡', route: '连接江南（无锡、苏州）的交通咽喉', price: '按车型/航程计算'})
           """)

            # 4. 创建关系：景点→城市
            session.run("""
               MATCH (a:Attraction), (c:City {name: '靖江市'})
               WHERE a.name IN ['孤山风景区', '牧城公园']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建关系：城市→推荐美食
            session.run("""
               MATCH (c:City {name: '靖江市'}), (f:Food)
               WHERE f.name IN ['靖江蟹黄汤包', '长江江鲜', '猪肉脯']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建关系：景点→附近美食
            session.run("""
               MATCH (a:Attraction), (f:Food {name: '靖江蟹黄汤包'})
               WHERE a.name IN ['孤山风景区', '牧城公园']
               CREATE (a)-[:NEAR_FOOD {distance: '约8km', description: '南园宾馆、鸿运酒楼等老字号可品尝正宗风味'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '牧城公园'}), (f:Food {name: '长江江鲜'})
               CREATE (a)-[:NEAR_FOOD {distance: '约3km', description: '江边餐馆可品尝新鲜江鲜'}]->(f)
           """)

            # 7. 创建关系：景点→附近住宿
            session.run("""
               MATCH (a:Attraction {name: '牧城公园'}), (ac:Accommodation {name: '靖江金悦国际酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '约5km', description: '位于江边，位置优越'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '孤山风景区'}), (ac:Accommodation {name: '靖江扬子江大酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '约10km'}]->(ac)
           """)

            # 8. 创建关系：城市→交通
            session.run("""
               MATCH (c:City {name: '靖江市'}), (t:Transportation)
               WHERE t.name IN ['靖江公交线路', '江阴长江大桥/靖江汽渡']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)

        print("靖江市旅游数据导入完成！")

    def import_taixing_data(self):
        """导入泰兴市旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (tx:City {name: '泰兴市', level: '县级市（由泰州市代管）', description: '位于江苏省中部、长江下游北岸，是江苏省直管县三个试点之一，教育、文化底蕴深厚，被誉为“教育之乡”、“银杏之乡”'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (huangqiao:Attraction {name: '黄桥古镇', type: '人文景观（红色旅游）', rating: 4.5, opening_hours: '全天开放（内部景点时间不一）'}),
               (yinxingsenlin:Attraction {name: '古银杏森林公园', type: '自然景观', rating: 4.4, opening_hours: '全天开放（最佳观赏期秋季）'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (shaobing:Food {name: '黄桥烧饼', type: '地方特产', price_range: '低', description: '色泽金黄，外酥内软，有咸甜多种口味，闻名全国'}),
               (baiguo:Food {name: '银杏（白果）', type: '地方特产', price_range: '低', description: '糯软香甜，可盐焗、可入菜，营养丰富'}),
               (jiangshaxie:Food {name: '江沙蟹', type: '地方特色', price_range: '中', description: '生长于江边沙土，壳青肚白，肉质鲜甜'}),
               (wendemu:Accommodation {name: '泰兴温德姆至尊酒店', type: '五星级酒店', price_range: '高', rating: 4.5}),
               (huangqiaobin:Accommodation {name: '黄桥宾馆', type: '商务酒店', price_range: '中', rating: 4.2}),
               (txgongjiao:Transportation {name: '泰兴公交线路', type: '公交', route: '覆盖城区及主要乡镇', price: '1-3元'}),
               (txkeyun:Transportation {name: '泰兴客运站', type: '大巴', route: '连通泰州、无锡、常州、上海等地', price: '按里程计算'})
           """)

            # 4. 创建关系：景点→城市
            session.run("""
               MATCH (a:Attraction), (c:City {name: '泰兴市'})
               WHERE a.name IN ['黄桥古镇', '古银杏森林公园']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建关系：城市→推荐美食
            session.run("""
               MATCH (c:City {name: '泰兴市'}), (f:Food)
               WHERE f.name IN ['黄桥烧饼', '银杏（白果）', '江沙蟹']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建关系：景点→附近美食
            session.run("""
               MATCH (a:Attraction {name: '黄桥古镇'}), (f:Food {name: '黄桥烧饼'})
               CREATE (a)-[:NEAR_FOOD {distance: '0.3km', description: '古镇内可购买最正宗口味'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '古银杏森林公园'}), (f:Food {name: '银杏（白果）'})
               CREATE (a)-[:NEAR_FOOD {distance: '0.5km', description: '园区周边可品尝银杏制品'}]->(f)
           """)

            # 7. 创建关系：景点→附近住宿
            session.run("""
               MATCH (a:Attraction {name: '黄桥古镇'}), (ac:Accommodation {name: '黄桥宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '0.8km', description: '位于古镇内，出行便利'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '古银杏森林公园'}), (ac:Accommodation {name: '泰兴温德姆至尊酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '约25km', description: '需返回市区住宿'}]->(ac)
           """)

            # 8. 创建关系：城市→交通
            session.run("""
               MATCH (c:City {name: '泰兴市'}), (t:Transportation)
               WHERE t.name IN ['泰兴公交线路', '泰兴客运站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)

        print("泰兴市旅游数据导入完成！")

    def import_hangzhou_data(self):
        """导入杭州市旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (hz:City {name: '杭州市', level: '新一线城市', description: '浙江省省会，中国七大古都之一，被誉为“人间天堂”。以西湖风光、互联网科技和深厚的文化底蕴闻名于世，是吴越文化和江南水乡的典型代表'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (xihu:Attraction {name: '西湖风景区', type: '自然+人文景观', rating: 4.8, opening_hours: '全天开放'}),
               (lingyin:Attraction {name: '灵隐寺', type: '人文景观', rating: 4.7, opening_hours: '7:00-18:15'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (xihucuoyu:Food {name: '西湖醋鱼', type: '杭帮菜', price_range: '中', description: '鱼肉鲜嫩，酸甜清香，带有蟹味'}),
               (dongporou:Food {name: '东坡肉', type: '杭帮菜', price_range: '中', description: '色泽红亮，皮糯肉酥，入口即化'}),
               (xihuguobin:Accommodation {name: '杭州西湖国宾馆', type: '国宾馆', price_range: '高', rating: 4.8}),
               (fayunanman:Accommodation {name: '杭州法云安缦', type: '奢华度假村', price_range: '高', rating: 4.7}),
               (ditie1:Transportation {name: '杭州地铁1号线', type: '地铁', route: '湘湖-萧山国际机场', price: '2-9元'}),
               (jichangdaba:Transportation {name: '杭州萧山国际机场大巴', type: '大巴', route: '机场-市区（武林门、城站等）', price: '20元'})
           """)

            # 4. 创建关系：景点→城市
            session.run("""
               MATCH (a:Attraction), (c:City {name: '杭州市'})
               WHERE a.name IN ['西湖风景区', '灵隐寺']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建关系：城市→推荐美食
            session.run("""
               MATCH (c:City {name: '杭州市'}), (f:Food)
               WHERE f.name IN ['西湖醋鱼', '东坡肉']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建关系：景点→附近美食
            session.run("""
               MATCH (a:Attraction {name: '西湖风景区'}), (f:Food)
               WHERE f.name IN ['西湖醋鱼', '东坡肉']
               CREATE (a)-[:NEAR_FOOD {distance: '约1km', description: '楼外楼、山外山等老字号杭帮菜馆可品尝'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '灵隐寺'}), (f:Food {name: '东坡肉'})
               CREATE (a)-[:NEAR_FOOD {distance: '约5km', description: '景区周边餐馆可品尝'}]->(f)
           """)

            # 7. 创建关系：景点→附近住宿
            session.run("""
               MATCH (a:Attraction {name: '西湖风景区'}), (ac:Accommodation {name: '杭州西湖国宾馆'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '约0.8km', description: '位于西湖核心区，景观绝佳'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '灵隐寺'}), (ac:Accommodation {name: '杭州法云安缦'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '约1.5km', description: '毗邻景区，环境清幽'}]->(ac)
           """)

            # 8. 创建关系：城市→交通
            session.run("""
               MATCH (c:City {name: '杭州市'}), (t:Transportation)
               WHERE t.name IN ['杭州地铁1号线', '杭州萧山国际机场大巴']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)

        print("杭州市旅游数据导入完成！")

    def import_ningbo_data(self):
        """导入宁波市旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (nb:City {name: '宁波市', level: '新一线城市', description: '浙江省副省级市，世界第四大港口城市，国家历史文化名城，是“海上丝绸之路”东方始发港。被誉为“书藏古今，港通天下”'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (tianyi:Attraction {name: '天一阁·月湖景区', type: '人文景观', rating: 4.7, opening_hours: '8:30-17:30'}),
               (xikou:Attraction {name: '溪口风景区', type: '自然+人文景观', rating: 4.6, opening_hours: '8:00-17:00'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (tangyuan:Food {name: '宁波汤圆', type: '小吃', price_range: '低', description: '皮薄馅多，香甜糯滑，以黑芝麻猪油馅为代表'}),
               (honggao:Food {name: '红膏炝蟹', type: '宁波菜', price_range: '中', description: '咸鲜合一，蟹膏艳红，肉质晶莹，是经典冷菜'}),
               (baiyue:Accommodation {name: '宁波柏悦酒店', type: '五星级度假酒店', price_range: '高', rating: 4.7}),
               (weistining:Accommodation {name: '宁波威斯汀酒店', type: '五星级酒店', price_range: '高', rating: 4.6}),
               (ditie2:Transportation {name: '宁波地铁2号线', type: '地铁', route: '栎社国际机场-清水浦', price: '2-8元'}),
               (guochangdaba:Transportation {name: '宁波栎社国际机场大巴', type: '大巴', route: '机场-市区（民航售票处）', price: '12元'})
           """)

            # 4. 创建关系：景点→城市
            session.run("""
               MATCH (a:Attraction), (c:City {name: '宁波市'})
               WHERE a.name IN ['天一阁·月湖景区', '溪口风景区']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建关系：城市→推荐美食
            session.run("""
               MATCH (c:City {name: '宁波市'}), (f:Food)
               WHERE f.name IN ['宁波汤圆', '红膏炝蟹']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建关系：景点→附近美食
            session.run("""
               MATCH (a:Attraction {name: '天一阁·月湖景区'}), (f:Food)
               WHERE f.name IN ['宁波汤圆', '红膏炝蟹']
               CREATE (a)-[:NEAR_FOOD {distance: '约2km', description: '城隍庙、南塘老街可品尝地道宁波小吃'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '溪口风景区'}), (f:Food {name: '宁波汤圆'})
               CREATE (a)-[:NEAR_FOOD {distance: '约1km', description: '景区周边小吃店可品尝'}]->(f)
           """)

            # 7. 创建关系：景点→附近住宿
            session.run("""
               MATCH (a:Attraction {name: '溪口风景区'}), (ac:Accommodation {name: '宁波柏悦酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '约30km', description: '位于东钱湖畔，适合度假'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '天一阁·月湖景区'}), (ac:Accommodation {name: '宁波威斯汀酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '约3km', description: '市区核心位置，出行便利'}]->(ac)
           """)

            # 8. 创建关系：城市→交通
            session.run("""
               MATCH (c:City {name: '宁波市'}), (t:Transportation)
               WHERE t.name IN ['宁波地铁2号线', '宁波栎社国际机场大巴']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)

        print("宁波市旅游数据导入完成！")

    def import_wenzhou_data(self):
        """导入温州市旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (wz:City {name: '温州市', level: '二线城市', description: '浙江省地级市，中国民营经济先发地区与改革开放前沿阵地，以“温州模式”和“东方犹太人”的经商智慧闻名。同时拥有雁荡山等绝美山水'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (yandang:Attraction {name: '雁荡山风景区', type: '自然景观', rating: 4.7, opening_hours: '全天开放（各景点时间不一）'}),
               (jiangxin:Attraction {name: '江心屿', type: '自然+人文景观', rating: 4.5, opening_hours: '8:00-22:00'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (yuwan:Food {name: '温州鱼丸', type: '小吃', price_range: '低', description: '以鱼肉加淀粉制成，呈不规则的条状，口感Q弹，汤味鲜美'}),
               (nuomifan:Food {name: '糯米饭', type: '小吃', price_range: '低', description: '蒸熟的糯米饭配上油条、肉末汤等，是温州人经典的早餐'}),
               (xianggelila:Accommodation {name: '温州香格里拉大酒店', type: '五星级酒店', price_range: '高', rating: 4.6}),
               (wzweistining:Accommodation {name: '温州威斯汀酒店', type: '五星级酒店', price_range: '高', rating: 4.5}),
               (guidao:Transportation {name: '温州轨道交通S1线', type: '市域铁路', route: '桐岭-双瓯大道', price: '2-13元'}),
               (longwandaba:Transportation {name: '温州龙湾国际机场大巴', type: '大巴', route: '机场-市区（民航售票处）', price: '15元'})
           """)

            # 4. 创建关系：景点→城市
            session.run("""
               MATCH (a:Attraction), (c:City {name: '温州市'})
               WHERE a.name IN ['雁荡山风景区', '江心屿']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建关系：城市→推荐美食
            session.run("""
               MATCH (c:City {name: '温州市'}), (f:Food)
               WHERE f.name IN ['温州鱼丸', '糯米饭']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建关系：景点→附近美食
            session.run("""
               MATCH (a:Attraction {name: '江心屿'}), (f:Food)
               WHERE f.name IN ['温州鱼丸', '糯米饭']
               CREATE (a)-[:NEAR_FOOD {distance: '约1.5km', description: '朔门街、天一角食街可品尝温州小吃'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '雁荡山风景区'}), (f:Food {name: '温州鱼丸'})
               CREATE (a)-[:NEAR_FOOD {distance: '约3km', description: '景区周边餐馆可品尝'}]->(f)
           """)

            # 7. 创建关系：景点→附近住宿
            session.run("""
               MATCH (a:Attraction {name: '江心屿'}), (ac:Accommodation {name: '温州香格里拉大酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '约2km', description: '位于瓯江畔，近景区'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '雁荡山风景区'}), (ac:Accommodation {name: '温州威斯汀酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '约70km', description: '需返回市区住宿'}]->(ac)
           """)

            # 8. 创建关系：城市→交通
            session.run("""
               MATCH (c:City {name: '温州市'}), (t:Transportation)
               WHERE t.name IN ['温州轨道交通S1线', '温州龙湾国际机场大巴']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)

        print("温州市旅游数据导入完成！")

    def import_jiaxing_data(self):
        """导入嘉兴市旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (jx:City {name: '嘉兴市', level: '三线城市', description: '位于浙江省东北部，是中国共产党诞生地，也是国家历史文化名城，素有“鱼米之乡”、“丝绸之府”的美誉，大运河穿城而过'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (nanhu:Attraction {name: '南湖旅游区', type: '自然+人文景观（红色旅游）', rating: 4.7, opening_hours: '8:00-17:00'}),
               (wuzhen:Attraction {name: '乌镇', type: '人文景观', rating: 4.7, opening_hours: '西栅9:00-22:00，东栅 夏令7:00-18:00，冬令7:00-17:30'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (zongzi:Food {name: '嘉兴粽子', type: '小吃', price_range: '低', description: '以鲜肉粽最为出名，糯而不烂，肥而不腻'}),
               (nanhuling:Food {name: '南湖菱', type: '地方特产', price_range: '低', description: '无角菱，皮色翠绿，肉质鲜嫩，可生食'}),
               (fupeng:Accommodation {name: '嘉兴福朋喜来登酒店', type: '商务酒店', price_range: '中高', rating: 4.5}),
               (wuzhenminsu:Accommodation {name: '乌镇民宿', type: '特色住宿', price_range: '中', rating: 4.6}),
               (youguidianche:Transportation {name: '嘉兴有轨电车', type: '有轨电车', route: '嘉兴南站-中山东路安乐路', price: '2元'}),
               (jiaxingnan:Transportation {name: '嘉兴南站', type: '高铁', route: '沪杭高铁线，连通上海、杭州', price: '按里程计算'})
           """)

            # 4. 创建关系：景点→城市
            session.run("""
               MATCH (a:Attraction), (c:City {name: '嘉兴市'})
               WHERE a.name IN ['南湖旅游区', '乌镇']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建关系：城市→推荐美食
            session.run("""
               MATCH (c:City {name: '嘉兴市'}), (f:Food)
               WHERE f.name IN ['嘉兴粽子', '南湖菱']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建关系：景点→附近美食
            session.run("""
               MATCH (a:Attraction {name: '南湖旅游区'}), (f:Food {name: '嘉兴粽子'})
               CREATE (a)-[:NEAR_FOOD {distance: '约2km', description: '五芳斋老字号可品尝'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '乌镇'}), (f:Food)
               WHERE f.name IN ['嘉兴粽子', '南湖菱']
               CREATE (a)-[:NEAR_FOOD {distance: '约0.5km', description: '古镇内可体验特色美食'}]->(f)
           """)

            # 7. 创建关系：景点→附近住宿
            session.run("""
               MATCH (a:Attraction {name: '南湖旅游区'}), (ac:Accommodation {name: '嘉兴福朋喜来登酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '约3km', description: '位于南湖新区，交通便利'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '乌镇'}), (ac:Accommodation {name: '乌镇民宿'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '0.3km', description: '古镇内特色住宿'}]->(ac)
           """)

            # 8. 创建关系：城市→交通
            session.run("""
               MATCH (c:City {name: '嘉兴市'}), (t:Transportation)
               WHERE t.name IN ['嘉兴有轨电车', '嘉兴南站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)

        print("嘉兴市旅游数据导入完成！")

    def import_huzhou_data(self):
        """导入湖州市旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (hz:City {name: '湖州市', level: '三线城市', description: '位于浙江省北部，太湖南岸，因湖得名，是“绿水青山就是金山银山”理念的诞生地。被誉为“中国毛笔之都”、“民国文化城”'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (nanxun:Attraction {name: '南浔古镇', type: '人文景观', rating: 4.7, opening_hours: '8:00-17:00'}),
               (moganshan:Attraction {name: '莫干山风景区', type: '自然景观', rating: 4.7, opening_hours: '全天开放'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (hundun:Food {name: '湖州大馄饨', type: '小吃', price_range: '低', description: '皮薄馅多，汤底鲜美，常用猪油调味'}),
               (qianzhangbao:Food {name: '丁莲芳千张包', type: '小吃', price_range: '低', description: '用千张（薄豆皮）包裹肉馅，鲜香可口'}),
               (baiyuyan:Food {name: '百鱼宴', type: '地方特色', price_range: '中高', description: '以太湖盛产的鱼类为原料，烹制出上百种菜肴'}),
               (dongwu:Accommodation {name: '湖州东吴开元名都酒店', type: '五星级酒店', price_range: '高', rating: 4.6}),
               (luoxingu:Accommodation {name: '莫干山裸心谷', type: '高端度假村', price_range: '高', rating: 4.7}),
               (huzhougongjiao:Transportation {name: '湖州公交线路', type: '公交', route: '覆盖城区', price: '1-2元'}),
               (huzhouzhan:Transportation {name: '湖州站', type: '高铁', route: '宁杭高铁线，连通杭州、南京', price: '按里程计算'})
           """)

            # 4. 创建关系：景点→城市
            session.run("""
               MATCH (a:Attraction), (c:City {name: '湖州市'})
               WHERE a.name IN ['南浔古镇', '莫干山风景区']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建关系：城市→推荐美食
            session.run("""
               MATCH (c:City {name: '湖州市'}), (f:Food)
               WHERE f.name IN ['湖州大馄饨', '丁莲芳千张包', '百鱼宴']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建关系：景点→附近美食
            session.run("""
               MATCH (a:Attraction {name: '南浔古镇'}), (f:Food)
               WHERE f.name IN ['湖州大馄饨', '丁莲芳千张包']
               CREATE (a)-[:NEAR_FOOD {distance: '约1km', description: '古镇周边可品尝传统小吃'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '莫干山风景区'}), (f:Food {name: '百鱼宴'})
               CREATE (a)-[:NEAR_FOOD {distance: '约15km', description: '山下餐馆可体验特色宴席'}]->(f)
           """)

            # 7. 创建关系：景点→附近住宿
            session.run("""
               MATCH (a:Attraction {name: '莫干山风景区'}), (ac:Accommodation {name: '莫干山裸心谷'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '约5km', description: '位于度假区内，环境清幽'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '南浔古镇'}), (ac:Accommodation {name: '湖州东吴开元名都酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '约30km', description: '位于市区，适合返程住宿'}]->(ac)
           """)

            # 8. 创建关系：城市→交通
            session.run("""
               MATCH (c:City {name: '湖州市'}), (t:Transportation)
               WHERE t.name IN ['湖州公交线路', '湖州站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)

        print("湖州市旅游数据导入完成！")

    def import_shaoxing_data(self):
        """导入绍兴市旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (sx:City {name: '绍兴市', level: '三线城市', description: '位于浙江省中北部，是著名的水乡、桥乡、酒乡、书法之乡、名士之乡，被誉为“文物之邦、鱼米之乡”，是鲁迅、周恩来的故乡'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (luxun:Attraction {name: '鲁迅故里', type: '人文景观', rating: 4.7, opening_hours: '8:30-17:00'}),
               (shenyuan:Attraction {name: '沈园', type: '人文景观', rating: 4.5, opening_hours: '8:00-17:00（白天），18:30-21:00（夜游）'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (choudoufu:Food {name: '绍兴臭豆腐', type: '小吃', price_range: '低', description: '外酥里嫩，闻着臭吃着香，是街头经典'}),
               (huangjiu:Food {name: '绍兴黄酒', type: '地方特产', price_range: '中', description: '香气浓郁，醇厚甘甜，可直接饮用或入菜'}),
               (huixiangdou:Food {name: '茴香豆', type: '小吃', price_range: '低', description: '孔乙己的“标配”，软糯咸香，是绝佳的下酒菜'}),
               (xianheng:Accommodation {name: '绍兴咸亨酒店', type: '特色酒店', price_range: '中高', rating: 4.6}),
               (dayukaiyuan:Accommodation {name: '绍兴大禹开元观堂', type: '度假村', price_range: '高', rating: 4.7}),
               (sxmetro:Transportation {name: '绍兴地铁1号线', type: '地铁', route: '芳泉-姑娘桥（与杭州地铁衔接）', price: '2-13元'}),
               (shaoxingbei:Transportation {name: '绍兴北站', type: '高铁', route: '杭甬高铁线，连通杭州、宁波', price: '按里程计算'})
           """)

            # 4. 创建关系：景点→城市
            session.run("""
               MATCH (a:Attraction), (c:City {name: '绍兴市'})
               WHERE a.name IN ['鲁迅故里', '沈园']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建关系：城市→推荐美食
            session.run("""
               MATCH (c:City {name: '绍兴市'}), (f:Food)
               WHERE f.name IN ['绍兴臭豆腐', '绍兴黄酒', '茴香豆']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建关系：景点→附近美食
            session.run("""
               MATCH (a:Attraction {name: '鲁迅故里'}), (f:Food)
               WHERE f.name IN ['绍兴臭豆腐', '绍兴黄酒', '茴香豆']
               CREATE (a)-[:NEAR_FOOD {distance: '0.5km', description: '景区内及仓桥直街可品尝地道风味'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '沈园'}), (f:Food {name: '绍兴黄酒'})
               CREATE (a)-[:NEAR_FOOD {distance: '约1km', description: '周边酒馆可体验黄酒文化'}]->(f)
           """)

            # 7. 创建关系：景点→附近住宿
            session.run("""
               MATCH (a:Attraction {name: '鲁迅故里'}), (ac:Accommodation {name: '绍兴咸亨酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '0.3km', description: '位于景区内，文化氛围浓厚'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '沈园'}), (ac:Accommodation {name: '绍兴大禹开元观堂'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '约8km', description: '水乡风格度假村'}]->(ac)
           """)

            # 8. 创建关系：城市→交通
            session.run("""
               MATCH (c:City {name: '绍兴市'}), (t:Transportation)
               WHERE t.name IN ['绍兴地铁1号线', '绍兴北站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)

        print("绍兴市旅游数据导入完成！")

    def import_taizhou_data(self):
        """导入台州旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (tz:City {name: '台州市', level: '三线城市', description: '位于浙江省中部沿海，是江南“水”乡，海上有名山。台州民营经济发达，是股份制经济的发源地之一，同时拥有以天台山为代表的秀美山水和海洋资源。'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (tiantaishan:Attraction {name: '天台山风景名胜区', type: '自然+人文景观', rating: 4.7, opening_hours: '8:00-17:00'}),
               (shenxianju:Attraction {name: '神仙居', type: '自然景观', rating: 4.7, opening_hours: '8:00-16:30'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (haixian:Food {name: '台州海鲜', type: '地方特色', price_range: '中', description: '地处东海渔场，海鲜种类丰富，做法原汁原味'}),
               (shibingtong:Food {name: '食饼筒', type: '小吃', price_range: '低', description: '一张面皮包裹多种菜肴，是台州特色主食，口感丰富'}),
               (jiangtangmian:Food {name: '姜汤面', type: '小吃', price_range: '中低', description: '用姜汁熬制汤底，配料丰富，味道辛辣鲜美，驱寒暖胃'}),
               (wanhao:Accommodation {name: '台州旗隆万豪酒店', type: '五星级酒店', price_range: '高', rating: 4.6}),
               (kaiyuan:Accommodation {name: '天台泰和开元名都大酒店', type: '商务酒店', price_range: '中', rating: 4.5}),
               (shiyuTieLu:Transportation {name: '台州市域铁路S1线', type: '轨道交通', route: '台州站-城南站', price: '2-14元'}),
               (gaotiezhan:Transportation {name: '台州站/台州西站', type: '高铁', route: '杭绍台高铁、甬台温铁路'})
           """)

            # 4. 创建关系：景点→城市
            session.run("""
               MATCH (a:Attraction), (c:City {name: '台州市'})
               WHERE a.name IN ['天台山风景名胜区', '神仙居']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建关系：城市→推荐美食
            session.run("""
               MATCH (c:City {name: '台州市'}), (f:Food)
               WHERE f.name IN ['台州海鲜', '食饼筒', '姜汤面']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建关系：景点→附近美食
            session.run("""
               MATCH (a:Attraction {name: '天台山风景名胜区'}), (f:Food {name: '台州海鲜'})
               CREATE (a)-[:NEAR_FOOD {note: '可前往椒江、路桥等区排挡餐馆品尝'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '神仙居'}), (f:Food {name: '台州海鲜'})
               CREATE (a)-[:NEAR_FOOD {note: '可前往椒江、路桥等区排挡餐馆品尝'}]->(f)
           """)

            # 7. 创建关系：景点→附近住宿
            session.run("""
               MATCH (a:Attraction {name: '天台山风景名胜区'}), (ac:Accommodation {name: '天台泰和开元名都大酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {distance: '较近'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '神仙居'}), (ac:Accommodation)
               WHERE ac.name IN ['台州旗隆万豪酒店']
               CREATE (a)-[:NEAR_ACCOMMODATION {note: '需返回仙居县城或选择景区周边民宿'}]->(ac)
           """)

            # 8. 创建关系：城市→交通
            session.run("""
               MATCH (c:City {name: '台州市'}), (t:Transportation)
               WHERE t.name IN ['台州市域铁路S1线', '台州站/台州西站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)

        print("台州旅游数据导入完成！")

    def import_lishui_data(self):
        """导入丽水旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (ls:City {name: '丽水市', level: '四线城市', description: '位于浙江省西南部，是浙江省陆域面积最大的地级市，被誉为“浙江绿谷”、“中国生态第一市”。境内群山叠翠，水系纵横，是摄影和生态旅游的胜地。'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (jinyunxiandu:Attraction {name: '缙云仙都', type: '自然+人文景观', rating: 4.7, opening_hours: '8:00-17:00'}),
               (yunhetitian:Attraction {name: '云和梯田', type: '自然+农业景观', rating: 4.6, opening_hours: '全天开放'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (jinyunshaobing:Food {name: '缙云烧饼', type: '小吃', price_range: '低', description: '用梅干菜和猪肉做馅，以炭火烤制，饼皮脆香'}),
               (anrenyutou:Food {name: '安仁鱼头', type: '地方特色', price_range: '中', description: '取自紧水滩水库的有机鱼，肉质鲜嫩，汤色奶白'}),
               (longquansunrong:Food {name: '龙泉笋茸', type: '地方特产', price_range: '中低', description: '用笋衣制成，口感脆嫩，是炖汤佳品'}),
               (huaqiaokaiyuan:Accommodation {name: '丽水华侨开元名都大酒店', type: '五星级酒店', price_range: '高', rating: 4.6}),
               (yunyideyuanzi:Accommodation {name: '云和云逸的院子别墅酒店', type: '特色民宿', price_range: '中高', rating: 4.7}),
               (gongjiao:Transportation {name: '丽水公交线路', type: '公交', route: '覆盖城区', price: '1-2元'}),
               (gaotieshan:Transportation {name: '丽水站', type: '高铁', route: '金温高铁线，连通温州、金华'})
           """)

            # 4. 创建关系：景点→城市
            session.run("""
               MATCH (a:Attraction), (c:City {name: '丽水市'})
               WHERE a.name IN ['缙云仙都', '云和梯田']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建关系：城市→推荐美食
            session.run("""
               MATCH (c:City {name: '丽水市'}), (f:Food)
               WHERE f.name IN ['缙云烧饼', '安仁鱼头', '龙泉笋茸']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建关系：景点→附近美食
            session.run("""
               MATCH (a:Attraction {name: '缙云仙都'}), (f:Food {name: '缙云烧饼'})
               CREATE (a)-[:NEAR_FOOD {note: '缙云县及仙都景区周边可品尝最正宗的缙云烧饼'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '云和梯田'}), (f:Food {name: '安仁鱼头'})
               CREATE (a)-[:NEAR_FOOD]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '云和梯田'}), (f:Food {name: '龙泉笋茸'})
               CREATE (a)-[:NEAR_FOOD]->(f)
           """)

            # 7. 创建关系：景点→附近住宿
            session.run("""
               MATCH (a:Attraction {name: '缙云仙都'}), (ac:Accommodation {name: '丽水华侨开元名都大酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '云和梯田'}), (ac:Accommodation {name: '云和云逸的院子别墅酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {note: '位于梯田景区'}]->(ac)
           """)

            # 8. 创建关系：城市→交通
            session.run("""
               MATCH (c:City {name: '丽水市'}), (t:Transportation)
               WHERE t.name IN ['丽水公交线路', '丽水站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)

        print("丽水旅游数据导入完成！")

    def import_jiande_data(self):
        """导入建德市旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (jd:City {name: '建德市', level: '县级市（由杭州市代管）', description: '位于浙江省西部，钱塘江上游，是杭州市下辖的县级市。以“奇山碧水”的旖旎风光和人文荟萃著称，是长三角的生态屏障，素有“锦峰绣岭、山水之乡”的美誉。'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (xinanjiang:Attraction {name: '新安江', type: '自然景观', rating: 4.6, opening_hours: '全天开放（游船等项目有时间限制）'}),
               (daciyan:Attraction {name: '大慈岩风景区（悬空寺）', type: '自然+人文景观', rating: 4.5, opening_hours: '8:00-16:30'}),
               (lingqidong:Attraction {name: '灵栖洞', type: '自然景观', rating: 4.4, opening_hours: '8:00-16:30'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (doufubao:Food {name: '建德豆腐包', type: '小吃', price_range: '低', description: '辣味独特，馅料以豆腐为主，鲜嫩入味，是建德早餐的灵魂'}),
               (gancaiya:Food {name: '严州干菜鸭', type: '地方特色', price_range: '中', description: '用干菜与鸭子一同烧制，肉质酥烂，干菜香浓，是严州府传统名菜'}),
               (jiuxingyutou:Food {name: '九姓鱼头王', type: '地方特色', price_range: '中', description: '以新安江有机鱼头为主料，汤汁奶白，鲜美微辣'}),
               (leidisong:Accommodation {name: '建德雷迪森怿曼酒店', type: '高端酒店', price_range: '中高', rating: 4.6}),
               (huangguan:Accommodation {name: '建德皇冠假日酒店', type: '商务酒店', price_range: '中', rating: 4.4}),
               (gongjiao:Transportation {name: '建德公交线路', type: '公交', route: '覆盖城区及主要乡镇', price: '1-4元'}),
               (gaotiezhan:Transportation {name: '建德站（高铁）', type: '高铁', route: '杭黄高铁线，连通杭州、黄山'})
           """)

            # 4. 创建关系：景点→城市
            session.run("""
               MATCH (a:Attraction), (c:City {name: '建德市'})
               WHERE a.name IN ['新安江', '大慈岩风景区（悬空寺）', '灵栖洞']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建关系：城市→推荐美食
            session.run("""
               MATCH (c:City {name: '建德市'}), (f:Food)
               WHERE f.name IN ['建德豆腐包', '严州干菜鸭', '九姓鱼头王']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建关系：景点→附近美食
            session.run("""
               MATCH (a:Attraction {name: '新安江'}), (f:Food)
               WHERE f.name IN ['建德豆腐包', '严州干菜鸭', '九姓鱼头王']
               CREATE (a)-[:NEAR_FOOD {note: '新安江畔及严州古城（梅城镇）可品尝地道建德风味'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '大慈岩风景区（悬空寺）'}), (f:Food)
               WHERE f.name IN ['建德豆腐包', '严州干菜鸭', '九姓鱼头王']
               CREATE (a)-[:NEAR_FOOD {note: '可前往严州古城（梅城镇）品尝地道风味'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '灵栖洞'}), (f:Food)
               WHERE f.name IN ['建德豆腐包', '严州干菜鸭', '九姓鱼头王']
               CREATE (a)-[:NEAR_FOOD {note: '可前往严州古城（梅城镇）品尝地道风味'}]->(f)
           """)

            # 7. 创建关系：景点→附近住宿
            session.run("""
               MATCH (a:Attraction {name: '新安江'}), (ac:Accommodation {name: '建德雷迪森怿曼酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {note: '位于江边'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '大慈岩风景区（悬空寺）'}), (ac:Accommodation {name: '建德皇冠假日酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '灵栖洞'}), (ac:Accommodation {name: '建德皇冠假日酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION]->(ac)
           """)

            # 8. 创建关系：城市→交通
            session.run("""
               MATCH (c:City {name: '建德市'}), (t:Transportation)
               WHERE t.name IN ['建德公交线路', '建德站（高铁）']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)

        print("建德市旅游数据导入完成！")

    def import_yuyao_data(self):
        """导入余姚市旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (yy:City {name: '余姚市', level: '县级市（由宁波市代管）', description: '位于浙江省东部，宁波市北部，是长江三角洲南翼的中心城市之一。余姚是中华文明的发祥地之一（河姆渡文化），素有“东南名邑”、“文献名邦”之称，也是王阳明、黄宗羲等思想家的故乡。'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (hemudu:Attraction {name: '河姆渡遗址博物馆', type: '人文景观', rating: 4.6, opening_hours: '9:00-16:30（周一闭馆）'}),
               (simingshan:Attraction {name: '四明山国家森林公园', type: '自然景观', rating: 4.5, opening_hours: '8:30-16:30'}),
               (wangyangming:Attraction {name: '王阳明故居', type: '人文景观', rating: 4.6, opening_hours: '8:30-16:30'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (yangmei:Food {name: '余姚杨梅', type: '地方特产', price_range: '中', description: '色泽艳丽，汁多味甜，是国家地理标志产品，成熟期为每年6月'}),
               (liangnongdagao:Food {name: '梁弄大糕', type: '传统茶食', price_range: '低', description: '糯米制成，印有吉祥图案，口感软糯香甜'}),
               (simenzaicai:Food {name: '泗门榨菜', type: '地方特产', price_range: '低', description: '口感脆嫩，鲜咸可口，是佐餐佳品'}),
               (taipingyang:Accommodation {name: '余姚太平洋大酒店', type: '五星级酒店', price_range: '高', rating: 4.5}),
               (chenmaohemudu:Accommodation {name: '余姚辰茂河姆渡酒店', type: '商务酒店', price_range: '中', rating: 4.3}),
               (gongjiao:Transportation {name: '余姚公交线路', type: '公交', route: '覆盖城区及主要乡镇', price: '1-3元'}),
               (yaoyaobeizhan:Transportation {name: '余姚北站', type: '高铁', route: '杭甬高铁线，连通杭州、宁波'})
           """)

            # 4. 创建关系：景点→城市
            session.run("""
               MATCH (a:Attraction), (c:City {name: '余姚市'})
               WHERE a.name IN ['河姆渡遗址博物馆', '四明山国家森林公园', '王阳明故居']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建关系：城市→推荐美食
            session.run("""
               MATCH (c:City {name: '余姚市'}), (f:Food)
               WHERE f.name IN ['余姚杨梅', '梁弄大糕', '泗门榨菜']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建关系：景点→附近美食
            session.run("""
               MATCH (a:Attraction {name: '四明山国家森林公园'}), (f:Food {name: '梁弄大糕'})
               CREATE (a)-[:NEAR_FOOD {note: '梁弄镇是购买和品尝梁弄大糕的首选地'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '河姆渡遗址博物馆'}), (f:Food)
               WHERE f.name IN ['余姚杨梅', '泗门榨菜']
               CREATE (a)-[:NEAR_FOOD]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '王阳明故居'}), (f:Food)
               WHERE f.name IN ['余姚杨梅', '梁弄大糕', '泗门榨菜']
               CREATE (a)-[:NEAR_FOOD]->(f)
           """)

            # 7. 创建关系：景点→附近住宿
            session.run("""
               MATCH (a:Attraction {name: '河姆渡遗址博物馆'}), (ac:Accommodation)
               WHERE ac.name IN ['余姚太平洋大酒店', '余姚辰茂河姆渡酒店']
               CREATE (a)-[:NEAR_ACCOMMODATION {note: '需返回市区'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '四明山国家森林公园'}), (ac:Accommodation {name: '余姚太平洋大酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '王阳明故居'}), (ac:Accommodation {name: '余姚辰茂河姆渡酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION]->(ac)
           """)

            # 8. 创建关系：城市→交通
            session.run("""
               MATCH (c:City {name: '余姚市'}), (t:Transportation)
               WHERE t.name IN ['余姚公交线路', '余姚北站']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)

        print("余姚市旅游数据导入完成！")

    def import_cixi_data(self):
        """导入慈溪市旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (cx:City {name: '慈溪市', level: '县级市（由宁波市代管）', description: '位于浙江省东部，宁波市北部，杭州湾南岸。是长江三角洲南翼重要的工商名城，也是“海上陶瓷之路”的重要起点，被誉为“家电之都”、“杨梅之乡”。'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (hangzhouwan:Attraction {name: '杭州湾国家湿地公园', type: '自然景观', rating: 4.5, opening_hours: '8:00-17:00'}),
               (mingheguzhen:Attraction {name: '鸣鹤古镇', type: '人文景观', rating: 4.4, opening_hours: '全天开放（内部景点时间不一）'}),
               (shanglinhu:Attraction {name: '上林湖越窑国家考古遗址公园', type: '人文景观', rating: 4.3, opening_hours: '9:00-16:30'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (cixiyangmei:Food {name: '慈溪杨梅', type: '地方特产', price_range: '中', description: '品种以荸荠种为主，果大核小，酸甜可口，是国家地理标志产品'}),
               (sanbeidousutang:Food {name: '三北豆酥糖', type: '传统茶食', price_range: '低', description: '香甜松脆，入口即化，有浓郁的黄豆香味'}),
               (longshanhongniluo:Food {name: '龙山黄泥螺', type: '地方特产', price_range: '中', description: '肉质鲜嫩，咸中带鲜，是经典的下饭菜'}),
               (huanqiuhotel:Accommodation {name: '慈溪杭州湾环球酒店', type: '五星级酒店', price_range: '高', rating: 4.6}),
               (hengyuanguangchang:Accommodation {name: '慈溪恒元广场酒店', type: '商务酒店', price_range: '中', rating: 4.4}),
               (gongjiao:Transportation {name: '慈溪公交线路', type: '公交', route: '覆盖城区及主要乡镇', price: '1-3元'}),
               (hangzhouwankaqia:Transportation {name: '杭州湾跨海大桥', type: '公路', route: '连接嘉兴（上海方向）与慈溪（宁波方向）'})
           """)

            # 4. 创建关系：景点→城市
            session.run("""
               MATCH (a:Attraction), (c:City {name: '慈溪市'})
               WHERE a.name IN ['杭州湾国家湿地公园', '鸣鹤古镇', '上林湖越窑国家考古遗址公园']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建关系：城市→推荐美食
            session.run("""
               MATCH (c:City {name: '慈溪市'}), (f:Food)
               WHERE f.name IN ['慈溪杨梅', '三北豆酥糖', '龙山黄泥螺']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建关系：景点→附近美食
            session.run("""
               MATCH (a:Attraction {name: '鸣鹤古镇'}), (f:Food {name: '三北豆酥糖'})
               CREATE (a)-[:NEAR_FOOD {note: '鸣鹤古镇内可品尝三北豆酥糖等传统小吃'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '杭州湾国家湿地公园'}), (f:Food)
               WHERE f.name IN ['慈溪杨梅', '龙山黄泥螺']
               CREATE (a)-[:NEAR_FOOD]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '上林湖越窑国家考古遗址公园'}), (f:Food)
               WHERE f.name IN ['慈溪杨梅', '三北豆酥糖', '龙山黄泥螺']
               CREATE (a)-[:NEAR_FOOD]->(f)
           """)

            # 7. 创建关系：景点→附近住宿
            session.run("""
               MATCH (a:Attraction {name: '杭州湾国家湿地公园'}), (ac:Accommodation {name: '慈溪杭州湾环球酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {note: '位于杭州湾新区'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '鸣鹤古镇'}), (ac:Accommodation {name: '慈溪恒元广场酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '上林湖越窑国家考古遗址公园'}), (ac:Accommodation {name: '慈溪恒元广场酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION]->(ac)
           """)

            # 8. 创建关系：城市→交通
            session.run("""
               MATCH (c:City {name: '慈溪市'}), (t:Transportation)
               WHERE t.name IN ['慈溪公交线路', '杭州湾跨海大桥']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)

        print("慈溪市旅游数据导入完成！")

    def import_ruian_data(self):
        """导入瑞安市旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (ra:City {name: '瑞安市', level: '县级市（由温州市代管）', description: '位于浙江省东南部，飞云江下游南岸，是中国改革开放的前沿阵地，以“温州模式”的重要发祥地而闻名。同时，瑞安也是浙江重要的历史文化名城，素有“东南小邹鲁”之称。'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (yuhailou:Attraction {name: '玉海楼', type: '人文景观', rating: 4.5, opening_hours: '9:00-17:00'}),
               (tongxifengjingqu:Attraction {name: '桐溪风景区', type: '自然景观', rating: 4.3, opening_hours: '8:00-16:30'}),
               (huayan:Attraction {name: '花岩国家森林公园', type: '自然景观', rating: 4.4, opening_hours: '8:00-16:30'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (ruianzhayang:Food {name: '瑞安扎羊', type: '地方特色', price_range: '中高', description: '将整只羊去骨扎紧后红烧，肉质酥烂，香气浓郁，是宴席大菜'}),
               (shenchengwuxianggan:Food {name: '莘塍五香干', type: '地方特产', price_range: '低', description: '豆干紧实，五香味浓，是佐餐和下酒的佳品'}),
               (hulingniupai:Food {name: '湖岭牛排', type: '地方特色', price_range: '中', description: '不同于西餐牛排，采用中式卤制方法，带骨烹煮，肉质鲜香有嚼劲'}),
               (chenmaoyangguang:Accommodation {name: '瑞安辰茂阳光酒店', type: '商务酒店', price_range: '中', rating: 4.4}),
               (ruianguoji:Accommodation {name: '瑞安国际大酒店', type: '商务酒店', price_range: '中', rating: 4.3}),
               (gongjiao:Transportation {name: '瑞安公交线路', type: '公交', route: '覆盖城区及主要街道', price: '1-3元'}),
               (ruianzhan:Transportation {name: '瑞安站（高铁）', type: '高铁', route: '甬台温铁路，连通温州、宁波'})
           """)

            # 4. 创建关系：景点→城市
            session.run("""
               MATCH (a:Attraction), (c:City {name: '瑞安市'})
               WHERE a.name IN ['玉海楼', '桐溪风景区', '花岩国家森林公园']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建关系：城市→推荐美食
            session.run("""
               MATCH (c:City {name: '瑞安市'}), (f:Food)
               WHERE f.name IN ['瑞安扎羊', '莘塍五香干', '湖岭牛排']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建关系：景点→附近美食
            session.run("""
               MATCH (a:Attraction {name: '花岩国家森林公园'}), (f:Food {name: '湖岭牛排'})
               CREATE (a)-[:NEAR_FOOD {note: '湖岭镇是品尝地道湖岭牛排的首选地'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '玉海楼'}), (f:Food)
               WHERE f.name IN ['瑞安扎羊', '莘塍五香干']
               CREATE (a)-[:NEAR_FOOD]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '桐溪风景区'}), (f:Food)
               WHERE f.name IN ['瑞安扎羊', '莘塍五香干', '湖岭牛排']
               CREATE (a)-[:NEAR_FOOD]->(f)
           """)

            # 7. 创建关系：景点→附近住宿
            session.run("""
               MATCH (a:Attraction {name: '玉海楼'}), (ac:Accommodation {name: '瑞安辰茂阳光酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION {note: '位于市中心'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '桐溪风景区'}), (ac:Accommodation {name: '瑞安国际大酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '花岩国家森林公园'}), (ac:Accommodation {name: '瑞安国际大酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION]->(ac)
           """)

            # 8. 创建关系：城市→交通
            session.run("""
               MATCH (c:City {name: '瑞安市'}), (t:Transportation)
               WHERE t.name IN ['瑞安公交线路', '瑞安站（高铁）']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)

        print("瑞安市旅游数据导入完成！")

    def import_yueqing_data(self):
        """导入乐清市旅游数据"""
        with self.driver.session() as session:
            # 1. 创建城市节点
            session.run("""
               CREATE
               (yq:City {name: '乐清市', level: '县级市（由温州市代管）', description: '位于浙江省东南部，瓯江口北岸，是中国市场经济发育最早、经济发展最具活力的地区之一，被誉为“中国电器之都”。同时拥有国家级风景名胜区、世界地质公园——雁荡山。'})
           """)

            # 2. 创建景点节点
            session.run("""
               CREATE
               (beiyandang:Attraction {name: '雁荡山风景区（北雁荡山）', type: '自然景观', rating: 4.7, opening_hours: '全天开放（各景点时间不一）'}),
               (zhongyandang:Attraction {name: '中雁荡山风景区', type: '自然景观', rating: 4.4, opening_hours: '8:00-16:30'})
           """)

            # 3. 创建美食、住宿、交通节点
            session.run("""
               CREATE
               (yueqingnihan:Food {name: '乐清泥蚶', type: '海鲜', price_range: '中', description: '血蚶的一种，肉质鲜嫩，营养丰富，常用开水烫食'}),
               (qingjiangsanxianmian:Food {name: '清江三鲜面', type: '小吃', price_range: '中', description: '以清江渡一带最为出名，用料讲究，配料丰富，汤底鲜美'}),
               (yandangshishanwa:Food {name: '雁荡山石蛙', type: '地方特色', price_range: '中高', description: '生长于雁荡山溪涧，肉质细嫩，是高蛋白食材'}),
               (tianhaotiancheng:Accommodation {name: '乐清天豪天成大酒店', type: '五星级酒店', price_range: '高', rating: 4.6}),
               (yandangshanzhuang:Accommodation {name: '雁荡山山庄', type: '度假酒店', price_range: '中', rating: 4.4}),
               (gongjiao:Transportation {name: '乐清公交线路', type: '公交', route: '覆盖城区及主要乡镇', price: '1-4元'}),
               (yueqingzhan:Transportation {name: '乐清站（高铁）', type: '高铁', route: '甬台温铁路，连通温州、宁波'}),
               (yandangshanzhan:Transportation {name: '雁荡山站（高铁）', type: '高铁', route: '甬台温铁路，直达雁荡山景区'})
           """)

            # 4. 创建关系：景点→城市
            session.run("""
               MATCH (a:Attraction), (c:City {name: '乐清市'})
               WHERE a.name IN ['雁荡山风景区（北雁荡山）', '中雁荡山风景区']
               CREATE (a)-[:LOCATED_IN]->(c)
           """)

            # 5. 创建关系：城市→推荐美食
            session.run("""
               MATCH (c:City {name: '乐清市'}), (f:Food)
               WHERE f.name IN ['乐清泥蚶', '清江三鲜面', '雁荡山石蛙']
               CREATE (c)-[:RECOMMENDS_FOOD]->(f)
           """)

            # 6. 创建关系：景点→附近美食
            session.run("""
               MATCH (a:Attraction {name: '雁荡山风景区（北雁荡山）'}), (f:Food)
               WHERE f.name IN ['乐清泥蚶', '雁荡山石蛙']
               CREATE (a)-[:NEAR_FOOD {note: '雁荡山景区周边是品尝特色海鲜和石蛙的好去处'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '中雁荡山风景区'}), (f:Food {name: '清江三鲜面'})
               CREATE (a)-[:NEAR_FOOD {note: '清江镇及周边可品尝地道清江三鲜面'}]->(f)
           """)
            session.run("""
               MATCH (a:Attraction {name: '中雁荡山风景区'}), (f:Food {name: '雁荡山石蛙'})
               CREATE (a)-[:NEAR_FOOD {note: '景区周边可品尝特色石蛙'}]->(f)
           """)

            # 7. 创建关系：景点→附近住宿
            session.run("""
               MATCH (a:Attraction {name: '雁荡山风景区（北雁荡山）'}), (ac:Accommodation {name: '雁荡山山庄'})
               CREATE (a)-[:NEAR_ACCOMMODATION {note: '位于景区内'}]->(ac)
           """)
            session.run("""
               MATCH (a:Attraction {name: '中雁荡山风景区'}), (ac:Accommodation {name: '乐清天豪天成大酒店'})
               CREATE (a)-[:NEAR_ACCOMMODATION]->(ac)
           """)

            # 8. 创建关系：城市→交通
            session.run("""
               MATCH (c:City {name: '乐清市'}), (t:Transportation)
               WHERE t.name IN ['乐清公交线路', '乐清站（高铁）', '雁荡山站（高铁）']
               CREATE (c)-[:HAS_TRANSPORTATION]->(t)
           """)

        print("乐清市旅游数据导入完成！")


if __name__ == "__main__":
    importer = Neo4jDataImporter(**NEO4J_CONFIG)
    importer.clear_database()  # 解开注释，清空所有重复数据
    importer.import_data()     # 重新导入一次干净数据
    importer.import_hefei_data()  # 导入合肥市数据
    importer.import_wuhu_data()  # 导入芜湖市数据
    importer.import_bengbu_data()  # 导入蚌埠市数据
    importer.import_huainan_data()  # 导入淮南市数据
    importer.import_maanshan_data()  # 导入马鞍山市数据
    importer.import_huaibei_data()  # 导入淮北市数据
    importer.import_tongling_data()  # 导入铜陵市数据
    importer.import_anqing_data()  # 导入安庆市数据
    importer.import_huangshan_data()  # 导入黄山市数据
    importer.import_chuzhou_data()  # 导入滁州市数据
    importer.import_fuyang_data()  # 导入阜阳市数据
    importer.import_suzhou_data()  # 导入宿州市数据
    importer.import_liuan_data()  # 导入六安市数据
    importer.import_bozhou_data()  # 导入亳州市数据
    importer.import_chizhou_data()  # 导入池州市数据
    importer.import_xuancheng_data()  # 导入宣城市数据
    importer.import_chaohu_data()  # 导入巢湖市数据
    importer.import_wuwei_data()  # 导入无为市数据
    importer.import_tongcheng_data()  # 导入桐城市数据
    importer.import_qianshan_data()  # 导入潜山市数据
    importer.import_mingguang_data()  # 导入明光市数据
    importer.import_jieshou_data()  # 导入界首市数据
    importer.import_ningguo_data()  # 导入宁国市数据
    importer.import_guangde_data()  # 导入广德市数据
    importer.import_fuzhou_data()  # 导入福州市数据
    importer.import_xiamen_data()  # 导入厦门市数据
    importer.import_putian_data()  # 导入莆田市数据
    importer.import_sanming_data()  # 导入三明市数据
    importer.import_quanzhou_data()  # 导入泉州市数据
    importer.import_zhangzhou_data()  # 导入漳州市数据
    importer.import_nanping_data()  # 导入南平市数据
    importer.import_longyan_data()  # 导入龙岩市数据
    importer.import_ningde_data()  # 导入宁德市数据
    importer.import_fuqing_data()  # 导入福清市数据
    importer.import_yongan_data()  # 导入永安市数据
    importer.import_shishi_data()  # 导入石狮市数据
    importer.import_jinjiang_data()  # 导入晋江市数据
    importer.import_nanan_data()  # 导入南安市数据
    importer.import_shaowu_data()  # 导入邵武市数据
    importer.import_wuyishan_data()  # 导入武夷山市数据
    importer.import_jianou_data()  # 导入建瓯市数据
    importer.import_zhangping_data()  # 导入漳平市数据
    importer.import_fuan_data()  # 导入福安市数据
    importer.import_fuding_data()  # 导入福鼎市数据
    importer.import_beijing_data()  # 导入北京市数据
    importer.import_tianjin_data()  # 导入天津市数据
    importer.import_shanghai_data()  # 导入上海市数据
    importer.import_chongqing_data()  # 导入重庆市数据
    importer.import_shijiazhuang_data()  # 导入石家庄市数据
    importer.import_tangshan_data()  # 导入唐山市数据
    importer.import_qinhuangdao_data()  # 导入秦皇岛市数据
    importer.import_handan_data()  # 导入邯郸市数据
    importer.import_xingtai_data()  # 导入邢台市数据
    importer.import_baoding_data()  # 导入保定市数据
    importer.import_zhangjiakou_data()  # 导入张家口市数据
    importer.import_chengde_data()  # 导入承德市数据
    importer.import_cangzhou_data()  # 导入沧州市数据
    importer.import_langfang_data()  # 导入廊坊市数据
    importer.importhengshui_data()  # 导入衡水市数据
    importer.import_xinji_data()  # 导入辛集市数据
    importer.import_jinzhou_data()  # 导入晋州市数据
    importer.import_xinle_data()  # 导入新乐市数据
    importer.import_zunhua_data()  # 导入遵化市数据
    importer.import_qianan_data()  # 导入迁安市数据
    importer.import_luanzhou_data()  # 导入滦州市数据
    importer.import_wuan_data()  # 导入武安市数据
    importer.import_nangong_data()  # 导入南宫市数据
    importer.import_shahe_data()  # 导入沙河市数据
    importer.import_zhuozhou_data()  # 导入涿州市数据
    importer.import_dingzhou_data()  # 导入定州市数据
    importer.import_anguo_data()  # 导入安国市数据
    importer.import_gaobeidian_data()  # 导入高碑店市数据
    importer.import_pingquan_data()  # 导入平泉市数据
    importer.import_botou_data()  # 导入泊头市数据
    importer.import_renqiu_data()  # 导入任丘市数据
    importer.import_huanghua_data()  # 导入黄骅市数据
    importer.import_hebei_data()  # 导入河间市数据
    importer.import_bazhou_data()  # 导入霸州市数据
    importer.import_sanhe_data()  # 导入三河市数据
    importer.import_shenzhou_data()  # 导入深州市数据
    importer.import_taiyuan_data()  # 导入太原市数据
    importer.import_datong_data()  # 导入大同市数据
    importer.import_yangquan_data()  # 导入阳泉市数据
    importer.import_changzhi_data()  # 导入长治市数据
    importer.import_jincheng_data()  # 导入晋城市数据
    importer.import_shuozhou_data()  # 导入朔州市数据
    importer.import_jinzhong_data()  # 导入晋中市数据
    importer.import_yuncheng_data()  # 导入运城市数据
    importer.import_xinzhou_data()  # 导入忻州市数据
    importer.import_linfen_data()  # 导入临汾市数据
    importer.import_lvliang_data()  # 导入吕梁市数据
    importer.import_gujiao_data()  # 导入古交市数据
    importer.import_gaoping_data()  # 导入高平市数据
    importer.import_huairen_data()  # 导入怀仁市数据
    importer.import_jiexiu_data()  # 导入介休市数据
    importer.import_yongji_data()  # 导入永济市数据
    importer.import_hejin_data()  # 导入河津市数据
    importer.import_yuanping_data()  # 导入原平市数据
    importer.import_houma_data()  # 导入侯马市数据
    importer.import_huozhou_data()  # 导入霍州市数据
    importer.import_xiaoyi_data()  # 导入孝义市数据
    importer.import_fenyang_data()  # 导入汾阳市数据
    importer.import_huhehaote_data()  # 导入呼和浩特市数据
    importer.import_baotou_data()  # 导入包头市数据
    importer.import_wuhai_data()  # 导入乌海市数据
    importer.import_chifeng_data()  # 导入赤峰市数据
    importer.import_tongliao_data()  # 导入通辽市数据
    importer.import_eerduosi_data()  # 导入鄂尔多斯市数据
    importer.import_wulanchabu_data()  # 导入乌兰察布市数据
    importer.import_manzhouli_data()  # 导入满洲里市数据
    importer.import_yakeshi_data()  # 导入牙克石市数据
    importer.import_zhalantun_data()  # 导入扎兰屯市数据
    importer.import_eerguna_data()  # 导入额尔古纳市数据
    importer.import_genhe_data()  # 导入根河市数据
    importer.import_fengzhen_data()  # 导入丰镇市数据
    importer.import_wulanhaote_data()  # 导入乌兰浩特市数据
    importer.import_aershan_data()  # 导入阿尔山市数据
    importer.import_erlianhaote_data()  # 导入二连浩特市数据
    importer.import_xilinhaote_data()  # 导入锡林浩特市数据
    importer.import_shenyang_data()  # 导入沈阳市数据
    importer.import_dalian_data()  # 导入大连市数据
    importer.import_anshan_data()  # 导入鞍山市数据
    importer.import_fushun_data()  # 导入抚顺市数据
    importer.import_benxi_data()  # 导入本溪市数据
    importer.import_dandong_data()  # 导入丹东市数据
    importer.import_jinzhou_data()  # 导入锦州市数据
    importer.import_yingkou_data()  # 导入营口市数据
    importer.import_fuxin_data()  # 导入阜新市数据
    importer.import_liaoyang_data()  # 导入辽阳市数据
    importer.import_panjin_data()  # 导入盘锦市数据
    importer.import_tieling_data()  # 导入铁岭市数据
    importer.import_huludao_data()  # 导入葫芦岛市数据
    importer.import_xinmin_data()  # 导入新民市数据
    importer.import_wafangdian_data()  # 导入瓦房店市数据
    importer.import_zhuanghe_data()  # 导入庄河市数据
    importer.import_haicheng_data()  # 导入海城市数据
    importer.import_donggang_data()  # 导入东港市数据
    importer.import_fengcheng_data()  # 导入凤城市数据
    importer.import_linghai_data()  # 导入凌海市数据
    importer.import_beizhen_data()  # 导入北镇市数据
    importer.import_gaizhou_data()  # 导入盖州市数据
    importer.import_dashiqiao_data()  # 导入大石桥市数据
    importer.import_dengta_data()  # 导入灯塔市数据
    importer.import_diaobingshan_data()  # 导入调兵山市数据
    importer.import_kaiyuan_data()  # 导入开原市数据
    importer.import_beipiao_data()  # 导入北票市数据
    importer.import_lingyuan_data()  # 导入凌源市数据
    importer.import_xingcheng_data()  # 导入兴城市数据
    importer.import_changchun_data()  # 导入长春市数据
    importer.import_jilin_data()  # 导入吉林市数据
    importer.import_siping_data()  # 导入四平市数据
    importer.import_liaoyuan_data()  # 导入辽源市数据
    importer.import_tonghua_data()  # 导入通化市数据
    importer.import_baishan_data()  # 导入白山市数据
    importer.import_songyuan_data()  # 导入松原市数据
    importer.import_baicheng_data()  # 导入白城市数据
    importer.import_yushu_data()  # 导入榆树市数据
    importer.import_dehui_data()  # 导入德惠市数据
    importer.import_gongzhuling_data()  # 导入公主岭市数据
    importer.import_huadian_data()  # 导入桦甸市数据
    importer.import_shulan_data()  # 导入舒兰市数据
    importer.import_panshi_data()  # 导入磐石市数据
    importer.import_shuangliao_data()  # 导入双辽市数据
    importer.import_jian_data()  # 导入集安市数据
    importer.import_linjiang_data()  # 导入临江市数据
    importer.import_fuyu_data()  # 导入扶余市数据
    importer.import_taonan_data()  # 导入洮南市数据据
    importer.import_yanji_data()  # 导入延吉市数据
    importer.import_tumen_data()  # 导入图们市数据
    importer.import_dunhua_data()  # 导入敦化市数据
    importer.import_hunchun_data()  # 导入珲春市数据
    importer.import_longjing_data()  # 导入龙井市数据
    importer.import_helong_data()  # 导入和龙市数据
    importer.import_haerbin_data()  # 导入哈尔滨市数据
    importer.import_qiqihaer_data()  # 导入齐齐哈尔市数据
    importer.import_jixi_data()  # 导入鸡西市数据
    importer.import_hegang_data()  # 导入鹤岗市数据
    importer.import_shuangyashan_data()  # 导入双鸭山市数据
    importer.import_daqing_data()  # 导入大庆市数据
    importer.import_yichun_data()  # 导入伊春市数据
    importer.import_jiamusi_data()  # 导入佳木斯市数据
    importer.import_qitaihe_data()  # 导入七台河市数据
    importer.import_mudanjiang_data()  # 导入牡丹江市数据
    importer.import_heihe_data()  # 导入黑河市数据
    importer.import_suihua_data()  # 导入绥化市数据
    importer.import_shangzhi_data()  # 导入尚志市数据
    importer.import_wuchang_data()  # 导入五常市数据
    importer.import_nehe_data()  # 导入讷河市数据
    importer.import_hulin_data()  # 导入虎林市数据
    importer.import_mishan_data()  # 导入密山市数据
    importer.import_tieli_data()  # 导入铁力市数据
    importer.import_tongjiang_data()  # 导入同江市数据
    importer.import_fujin_data()  # 导入富锦市数据
    importer.import_fuyuan_data()  # 导入抚远市数据
    importer.import_suifenhe_data()  # 导入绥芬河市数据
    importer.import_hailin_data()  # 导入海林市数据
    importer.import_ningan_data()  # 导入宁安市数据
    importer.import_muling_data()  # 导入穆棱市数据
    importer.import_dongning_data()  # 导入东宁市数据
    importer.import_nenjiang_data()  # 导入嫩江市数据
    importer.import_zhaodong_data()  # 导入肇东市数据
    importer.import_hailun_data()  # 导入海伦市数据
    importer.import_mohe_data()  # 导入漠河市数据
    importer.import_nanjing_data()  # 导入南京市数据
    importer.import_wuxi_data()  # 导入无锡市数据
    importer.import_xuzhou_data()  # 导入徐州市数据
    importer.import_changzhou_data()  # 导入常州市数据
    importer.import_suzhou_data()  # 导入苏州市数据
    importer.import_nantong_data()  # 导入南通市数据
    importer.import_lianyungang_data()  # 导入连云港市数据
    importer.import_huaian_data()  # 导入淮安市数据
    importer.import_yancheng_data()  # 导入盐城市数据
    importer.import_yangzhou_data()  # 导入扬州市数据
    importer.import_zhenjiang_data()  # 导入镇江市数据
    importer.import_taizhou_data()  # 导入泰州市数据
    importer.import_suqian_data()  # 导入宿迁市数据
    importer.import_jiangyin_data()  # 导入江阴市数据
    importer.import_yixing_data()  # 导入宜兴市数据
    importer.import_xinyi_data()  # 导入新沂市数据
    importer.import_pizhou_data()  # 导入邳州市数据
    importer.import_liyang_data()  # 导入溧阳市数据
    importer.import_changshu_data()  # 导入常熟市数据
    importer.import_zhangjiagang_data()  # 导入张家港市数据
    importer.import_kunshan_data()  # 导入昆山市数据
    importer.import_taicang_data()  # 导入太仓市数据
    importer.import_qidong_data()  # 导入启东市数据
    importer.import_rugao_data()  # 导入如皋市数据
    importer.import_haian_data()  # 导入海安市数据
    importer.import_dongtai_data()  # 导入东台市数据
    importer.import_yizheng_data()  # 导入仪征市数据
    importer.import_gaoyou_data()  # 导入高邮市数据
    importer.import_danyang_data()  # 导入丹阳市数据
    importer.import_yangzhong_data()  # 导入扬中市数据
    importer.import_jurong_data()  # 导入句容市数据
    importer.import_xinghua_data()  # 导入兴化市数据
    importer.import_jingjiang_data()  # 导入靖江市数据
    importer.import_taixing_data()  # 导入泰兴市数据
    importer.import_hangzhou_data()  # 导入杭州市数据
    importer.import_ningbo_data()  # 导入宁波市数据
    importer.import_wenzhou_data()  # 导入温州市数据
    importer.import_jiaxing_data()  # 导入嘉兴市数据
    importer.import_huzhou_data()  # 导入湖州市数据
    importer.import_shaoxing_data()  # 导入绍兴市数据
    importer.import_taizhou_data()  # 导入台州市数据
    importer.import_lishui_data()  # 导入丽水市数据
    importer.import_jiande_data()  # 导入建德市数据
    importer.import_yuyao_data()  # 导入余姚市数据
    importer.import_cixi_data()  # 导入慈溪市数据
    importer.import_ruian_data()  # 导入瑞安市数据
    importer.close()