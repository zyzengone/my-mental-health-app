<template>
  <el-container class="knowledge-graph-container">
    <el-header>
      心理知识图谱展示
      <el-input
          placeholder="搜索疾病或症状"
          v-model="searchQuery"
          @input="filterGraph"
          style="width: 300px; margin-left: 20px;"
      />
    </el-header>
    <el-main>
      <!-- 使用 D3.js 绘制的图形表示 -->
      <div ref="chart" className="ggraph"></div>
    </el-main>
    <el-aside>
      <!-- 侧边栏，可以包含搜索框和过滤器 -->

    </el-aside>
  </el-container>
</template>

<script>
import * as d3 from 'd3';
import { getAllDisease } from "../api/knowledge.js";


export default {
  data() {
    return {
      searchQuery: '',
      nodes: [
        { id: 'Disease1', name:'抑郁', label: '疾病' },
        { id: 'Symptom1',name:'抓狂', label: '症状' },
        { id: 'Drug1',name:'药', label: '药物' },
        { id: 'Disease2', name:'焦虑', label: '疾病' },
        { id: 'Symptom2',name:'抓狂2', label: '症状' },
        { id: 'Drug2',name:'药2', label: '药物' },
      ],
      links: [
        { source: 'Disease1', target: 'Symptom1', relate: 'has_symptom' },
        { source: 'Disease1', target: 'Drug1', relate: 'common_drug' },
        { source: 'Disease2', target: 'Symptom2', relate: 'has_symptom' },
        { source: 'Disease2', target: 'Drug2', relate: 'common_drug' },
      ],
    };
  },
  mounted() {
    getAllDisease().then(res => {
      if (res.code === 200) {
        this.originalNodes = res.data.nodes;
        this.originalLinks = res.data.links;
        this.nodes = this.originalNodes;
        this.links = this.originalLinks;
        this.drawChart()
      }
    })

  },
  methods: {
    drawChart() {
      const data = {
        nodes: this.nodes,
        links: this.links
      };

      // 定义颜色映射（匹配 node.json 中的 label：symptom, disease）
      const colorMap = {
        'symptom': '#54b1aa',   // 症状 - 青色
        'disease': '#e3716e',  // 疾病 - 红色
        '药物': 'green'        // 备用
      };
      // 修改1: 增大画布尺寸
      const width = 1500;
      const height = 900;
      // 清除之前的图表
      d3.select(this.$refs.chart).selectAll('*').remove();
      // 创建SVG容器
      const svg = d3.select(this.$refs.chart)
          .append('svg')
          .attr('width', width)
          .attr('height', height);

      const g = svg.append('g'); // 将 g 元素放在 svg 元素内部

      // 修改2: 增加节点间距离和电荷力强度以减少重叠
      const simulation = d3.forceSimulation(data.nodes)
          .force('link', d3.forceLink(data.links).id(d => d.id).distance(150))
          .force('charge', d3.forceManyBody().strength(-300))
          .force('center', d3.forceCenter(width / 2, height / 2));
      // 创建边
      const link = g.selectAll('line')
          .data(data.links)
          .enter()
          .append('line')
          .attr('stroke', '#999')
          .attr('stroke-width', 2)
      //创建节点
      const node = g.selectAll('.node')
          .data(data.nodes)
          .enter()
          .append('g')
          .attr('class', 'node')
          .style('fill', d => colorMap[d.label] || '#999'); // 使用颜色映射

      // 修改3: 增大节点半径
      node.append('circle')
          .attr('r', 25)
          .attr('fill', d => colorMap[d.label] || '#999') // 根据 label 设置颜色，默认为灰色
          .call(d3.drag() // 节点拖拽
              .on('start', dragstarted)
              .on('drag', dragged)
              .on('end', dragended));
      //节点上面显示文字
      node.append('text')
          .text(d => d.name)
          .attr('text-anchor', 'middle')
          .attr('dy', 4)
          // 修改4: 调整字体大小
          .attr('font-size', d => Math.min(2 * 25, 8))
          .attr('fill', 'black')
          .style('pointer-events', 'none');
      // 连线文字
      const linkText = g.selectAll('.linktext')
          .data(data.links)
          .enter()
          .append('text')
          .attr('class', 'linktext')
          .style('fill', 'black')
          .style('font-size', 8)
          .style('text-anchor', 'middle')
          .text(d => d.relate)
          .style('pointer-events', 'none');

      // 缩放
      svg.call(d3.zoom().on("zoom", function (event) {
        g.attr("transform", event.transform);
      }));
      // 监听力导向图模拟器的tick事件，更新节点和边的位置
      simulation
          .on('tick', () => {
            link
                .attr('x1', d => d.source.x)
                .attr('y1', d => d.source.y)
                .attr('x2', d => d.target.x)
                .attr('y2', d => d.target.y);

            node.attr('transform', d => `translate(${d.x},${d.y})`);
            // 更新连线文字的位置
            linkText
                .attr('x', d => (d.source.x + d.target.x) / 2)
                .attr('y', d => (d.source.y + d.target.y) / 2);
          });

      function dragstarted(event, d) {
        if (!event.active) simulation.alphaTarget(0.5).restart();
        d.fx = d.x;
        d.fy = d.y;
      }

      function dragged(event, d) {
        d.fx = event.x;
        d.fy = event.y;
      }

      function dragended(event, d) {
        if (!event.active) simulation.alphaTarget(0);
        d.fx = null;
        d.fy = null;
      }
    },
    filterGraph() {
      const query = this.searchQuery.toLowerCase();
      const matchedNodes = this.originalNodes.filter(node =>
          node.name.toLowerCase().includes(query) ||
          node.label.toLowerCase().includes(query)
      );

      // 获取与匹配节点有关系的所有节点
      const relatedNodes = new Set(matchedNodes.map(node => node.id));
      const originMatchNodes = new Set(relatedNodes)
      console.log(matchedNodes)
      this.originalLinks.forEach(link => {
        if (originMatchNodes.has(link.source.id)) {
          relatedNodes.add(link.target.id);
        }
      });
      console.log(relatedNodes)
      const filteredNodes = this.originalNodes.filter(node => relatedNodes.has(node.id));

      // 更新边的 source 和 target 为节点对象
      const filteredLinks = this.originalLinks
          .filter(link => originMatchNodes.has(link.source.id) && relatedNodes.has(link.target.id));
      console.log(filteredNodes)
      console.log(filteredLinks)
      this.nodes = filteredNodes;
      this.links = filteredLinks;

      this.drawChart();
    },
  },
};
</script>

<style scoped>
.knowledge-graph-container {
  height: 100vh;
  display: flex;
  flex-direction: column;
}
#graph-container {
  flex-grow: 1;
  position: relative;
}
</style>