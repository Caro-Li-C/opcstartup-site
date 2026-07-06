layout: default
title: 加入社群
permalink: /community/
<style>
  .community-page {
    font-family: 'Noto Sans SC', system-ui, sans-serif;
    background-color: #faf8f5;
    color: #1a1a1a;
    padding-top: 0;
  }
  .community-page .section-title {
    position: relative;
    display: inline-block;
  }
  .community-page .section-title::after {
    content: '';
    position: absolute;
    bottom: -8px;
    left: 0;
    width: 40px;
    height: 2px;
    background-color: #c9a87c;
  }
  .community-page .faq-content {
    max-height: 0;
    overflow: hidden;
    transition: max-height 0.4s ease, padding 0.4s ease;
  }
  .community-page .faq-item.active .faq-content {
    max-height: 300px;
  }
  .community-page .faq-item.active .faq-icon {
    transform: rotate(45deg);
  }
  .community-page .group-card {
    transition: all 0.3s ease;
  }
  .community-page .group-card:hover {
    border-color: #c9a87c;
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(0,0,0,0.04);
  }
  .community-page .rule-card {
    transition: all 0.3s ease;
  }
  .community-page .rule-card:hover {
    border-color: #c9a87c;
  }
  .community-page .qr-card {
    box-shadow: 0 4px 20px rgba(0,0,0,0.06);
  }
  .community-page .not-for-you {
    background: linear-gradient(135deg, #fdf6f0 0%, #faf8f5 100%);
  }
  .community-page .hero-pattern {
    background-image: radial-gradient(circle at 1px 1px, rgba(201,168,124,0.15) 1px, transparent 0);
    background-size: 40px 40px;
  }
  .community-page .divider-ornament {
    display: flex;
    align-items: center;
    gap: 12px;
  }
  .community-page .divider-ornament::before,
  .community-page .divider-ornament::after {
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, transparent, #e8e4df, transparent);
  }
  .community-page .tag-pill {
    display: inline-flex;
    align-items: center;
    padding: 2px 10px;
    border-radius: 4px;
    font-size: 12px;
    background: #f5f0e8;
    color: #8c8c8c;
  }
  .community-page .tier-label {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-size: 11px;
    font-weight: 500;
    letter-spacing: 0.05em;
    text-transform: uppercase;
  }
  .community-page .tier-label .dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #c9a87c;
  }
  .community-page .tier-label .count {
    color: #8c8c8c;
    font-weight: 400;
  }
  .community-page .rule-step {
    display: flex;
    gap: 16px;
    padding: 16px 0;
    border-bottom: 1px solid #f0ebe3;
  }
  .community-page .rule-step:last-child {
    border-bottom: none;
  }
  .community-page .rule-step-num {
    width: 28px;
    height: 28px;
    border-radius: 50%;
    background: rgba(201,168,124,0.12);
    color: #c9a87c;
    font-size: 12px;
    font-weight: 600;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    margin-top: 2px;
  }
  .community-page .rule-highlight {
    background: #f5f0e8;
    border: 1px dashed #c9a87c;
    border-radius: 8px;
    padding: 12px 16px;
    font-family: monospace;
    font-size: 14px;
    color: #1a1a1a;
    display: inline-block;
    margin: 4px 0;
  }
  .community-page .rule-warning {
    background: #fdf6f0;
    border-left: 3px solid #c9a87c;
    padding: 12px 16px;
    border-radius: 0 8px 8px 0;
    margin-top: 8px;
  }

  /* === 社群矩阵改进样式 === */
  .community-page .region-block {
    border: 1px solid #e8e4df;
    border-radius: 16px;
    overflow: hidden;
    transition: all 0.3s ease;
    background: #fff;
  }
  .community-page .region-block:hover {
    border-color: #c9a87c;
    box-shadow: 0 8px 32px rgba(0,0,0,0.06);
    transform: translateY(-2px);
  }
  .community-page .region-header {
    background: #f5f0e8;
    padding: 16px 24px;
    display: flex;
    align-items: center;
    gap: 10px;
  }
  .community-page .region-header .region-name {
    font-weight: 600;
    font-size: 15px;
    color: #1a1a1a;
  }
  .community-page .region-header .region-tag {
    font-size: 12px;
    color: #8c8c8c;
    background: rgba(255,255,255,0.7);
    padding: 3px 10px;
    border-radius: 6px;
    border: 1px solid rgba(201,168,124,0.15);
  }
  .community-page .region-body {
    padding: 24px;
  }
  .community-page .city-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 8px 18px;
    border-radius: 24px;
    border: 1px solid #e8e4df;
    background: #fff;
    font-size: 14px;
    color: #1a1a1a;
    transition: all 0.2s ease;
    cursor: default;
  }
  .community-page .city-pill:hover {
    border-color: #c9a87c;
    background: #faf8f5;
  }
  .community-page .city-pill .status-dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: #c9a87c;
  }
  .community-page .fallback-row {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-top: 20px;
    padding-top: 16px;
    border-top: 1px dashed #e8e4df;
    font-size: 14px;
    color: #8c8c8c;
  }
  .community-page .fallback-row .fallback-link {
    color: #c9a87c;
    font-weight: 500;
  }
  .community-page .arrow-icon {
    color: #c9a87c;
    font-size: 14px;
  }

  /* 全国群特殊样式 */
  .community-page .national-card {
    border: 1px solid #e8e4df;
    border-radius: 16px;
    padding: 32px;
    background: #fff;
    transition: all 0.3s ease;
  }
  .community-page .national-card:hover {
    border-color: #c9a87c;
    box-shadow: 0 8px 32px rgba(0,0,0,0.06);
  }
  .community-page .national-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 6px 16px;
    border-radius: 20px;
    font-size: 13px;
    font-weight: 500;
    background: rgba(201,168,124,0.1);
    color: #c9a87c;
    border: 1px solid rgba(201,168,124,0.2);
  }
</style>
<div class="community-page">
  <!-- Hero -->
  <section class="pt-16 pb-10 px-6 relative overflow-hidden">
    <div class="absolute inset-0 hero-pattern opacity-60"></div>
    <div class="max-w-4xl mx-auto relative">
      <div class="flex items-center gap-3 mb-8 text-sm">
        <span class="tag-pill">社群</span>
        <span style="color: #e8e4df;">|</span>
        <span class="text-muted">OPC</span>
        <span style="color: #e8e4df;">|</span>
        <span class="text-muted">一人公司</span>
        <span class="flex-1"></span>
        <span class="text-muted text-xs">2026-07-02</span>
      </div>

      <div class="flex items-start gap-8">
        <div class="flex-1">
          <h1 class="text-3xl md:text-4xl font-bold mb-3 leading-tight tracking-tight" style="color: #1a1a1a;">加入社群</h1>
          <p style="color: #c9a87c;" class="text-base mb-8">与全国超级个体建立真实连接</p>
        </div>
        <div class="hidden md:flex gap-6 text-center">
          <div>
            <div class="text-5xl font-light" style="color: #c9a87c; line-height: 1;">39</div>
            <div class="text-xs text-muted mt-2">社群矩阵</div>
          </div>
          <div class="w-px" style="background: #e8e4df;"></div>
          <div>
            <div class="text-5xl font-light" style="color: #c9a87c; line-height: 1;">18</div>
            <div class="text-xs text-muted mt-2">城市覆盖</div>
          </div>
        </div>
      </div>

      <div class="border-l-4 rounded-r-lg p-6 mt-4" style="border-color: #c9a87c; background: #f5f0e8;">
        <p class="text-muted leading-relaxed text-base">
          欢迎来到【OPC创业汇】。这里是一个OPC创业者之间建立真实连接的网络。我们相信：最好的资源不是信息，而是彼此信任的人。
        </p>
        <p class="text-muted leading-relaxed text-base mt-3">
          已有成员通过OPC创业汇找到联合创始人、达成战略合作、接到订单，也有成员成功入驻到契合的社区。
        </p>
      </div>
    </div>
  </section>
  <!-- 适合人群 -->
  <section class="py-6 px-6">
    <div class="max-w-4xl mx-auto">
      <h2 class="section-title text-xl font-medium mb-4" style="color: #1a1a1a;">这里适合你，如果你</h2>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mt-6">
        <div class="bg-white border rounded-lg p-6 relative overflow-hidden" style="border-color: #e8e4df;">
          <div class="absolute top-4 right-4" style="color: rgba(201,168,124,0.1);">
            <svg class="w-12 h-12" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/></svg>
          </div>
          <div class="text-4xl font-light mb-4" style="color: rgba(201,168,124,0.3);">01</div>
          <p class="text-sm leading-relaxed" style="color: #1a1a1a;">正在<strong>独立运营自己的业务</strong></p>
        </div>
        <div class="bg-white border rounded-lg p-6 relative overflow-hidden" style="border-color: #e8e4df;">
          <div class="absolute top-4 right-4" style="color: rgba(201,168,124,0.1);">
            <svg class="w-12 h-12" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"/></svg>
          </div>
          <div class="text-4xl font-light mb-4" style="color: rgba(201,168,124,0.3);">02</div>
          <p class="text-sm leading-relaxed" style="color: #1a1a1a;">愿意<strong>分享真实经验</strong>，不只是成功</p>
        </div>
        <div class="bg-white border rounded-lg p-6 relative overflow-hidden" style="border-color: #e8e4df;">
          <div class="absolute top-4 right-4" style="color: rgba(201,168,124,0.1);">
            <svg class="w-12 h-12" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"/></svg>
          </div>
          <div class="text-4xl font-light mb-4" style="color: rgba(201,168,124,0.3);">03</div>
          <p class="text-sm leading-relaxed" style="color: #1a1a1a;">想找到可以<strong>长期合作的伙伴</strong>，不只是客户</p>
        </div>
      </div>
    </div>
  </section>
  <!-- 不适合人群 -->
  <section class="py-6 px-6">
    <div class="max-w-4xl mx-auto">
      <h2 class="section-title text-xl font-medium mb-4" style="color: #1a1a1a; opacity: 0.5;">这里不适合你，如果你</h2>
      <div class="not-for-you border rounded-lg p-6 mt-6 max-w-4xl" style="border-color: #e8e4df;">
        <ul class="space-y-4 text-muted text-sm">
          <li class="flex items-start gap-3">
            <div class="w-6 h-6 rounded-full flex items-center justify-center shrink-0 mt-0.5" style="background: rgba(26,26,26,0.05);">
              <span class="text-xs" style="color: rgba(26,26,26,0.3);">×</span>
            </div>
            <span>主要目的是推广产品</span>
          </li>
          <li class="flex items-start gap-3">
            <div class="w-6 h-6 rounded-full flex items-center justify-center shrink-0 mt-0.5" style="background: rgba(26,26,26,0.05);">
              <span class="text-xs" style="color: rgba(26,26,26,0.3);">×</span>
            </div>
            <span>不打算给别人提供任何价值</span>
          </li>
        </ul>
      </div>
    </div>
  </section>

  <!-- 社群矩阵 — 改进版：更舒展的排版 -->
  <section class="py-10 px-6">
    <div class="max-w-4xl mx-auto">
      <h2 class="section-title text-xl font-medium mb-8" style="color: #1a1a1a;">社群矩阵</h2>

      <div class="mt-8 space-y-8">

        <!-- 第一层：全国群 — 全宽突出 -->
        <div>
          <div class="tier-label mb-5">
            <span class="dot"></span>
            <span style="color: #1a1a1a;">全国群</span>
            <span class="count">核心 · 每人限加1个</span>
          </div>
          <div class="national-card">
            <div class="flex items-center justify-between mb-4">
              <span class="font-semibold text-lg" style="color: #1a1a1a;">OPC创业汇 · 全国总群</span>
              <span class="national-badge">开放加入</span>
            </div>
            <p class="text-sm text-muted leading-relaxed">覆盖全国OPC创业者，政策速递与资源对接。每人仅限加入一个全国群。</p>
          </div>
        </div>

        <!-- 分隔装饰 -->
        <div class="divider-ornament py-2">
          <span class="text-xs text-muted" style="letter-spacing: 0.2em;">属地社群</span>
        </div>

        <!-- 第二层：属地群 — 更宽松的网格 -->
        <div>
          <div class="tier-label mb-5">
            <span class="dot"></span>
            <span style="color: #1a1a1a;">属地群</span>
            <span class="count">6个区域/省份</span>
          </div>
          <p class="text-sm text-muted mb-6">找到你所在的城市或省份，有专属城市群则加入；没有则加入所属区域群。</p>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-5">

            <!-- 京津冀 -->
            <div class="region-block">
              <div class="region-header">
                <span class="region-name">京津冀</span>
                <span class="region-tag">2个城市群</span>
              </div>
              <div class="region-body">
                <div class="flex flex-wrap gap-3">
                  <span class="city-pill"><span class="status-dot"></span>北京</span>
                  <span class="city-pill"><span class="status-dot"></span>天津</span>
                </div>
                <div class="fallback-row">
                  <span class="arrow-icon">→</span>
                  <span>其他城市加入</span>
                  <span class="fallback-link">京津冀区域群</span>
                </div>
              </div>
            </div>

            <!-- 长三角 -->
            <div class="region-block">
              <div class="region-header">
                <span class="region-name">长三角</span>
                <span class="region-tag">4个城市群</span>
              </div>
              <div class="region-body">
                <div class="flex flex-wrap gap-3">
                  <span class="city-pill"><span class="status-dot"></span>上海</span>
                  <span class="city-pill"><span class="status-dot"></span>杭州</span>
                  <span class="city-pill"><span class="status-dot"></span>苏州</span>
                  <span class="city-pill"><span class="status-dot"></span>南京</span>
                </div>
                <div class="fallback-row">
                  <span class="arrow-icon">→</span>
                  <span>其他城市加入</span>
                  <span class="fallback-link">长三角区域群</span>
                </div>
              </div>
            </div>

            <!-- 大湾区 -->
            <div class="region-block">
              <div class="region-header">
                <span class="region-name">大湾区</span>
                <span class="region-tag">3个城市群</span>
              </div>
              <div class="region-body">
                <div class="flex flex-wrap gap-3">
                  <span class="city-pill"><span class="status-dot"></span>深圳</span>
                  <span class="city-pill"><span class="status-dot"></span>广州</span>
                  <span class="city-pill"><span class="status-dot"></span>香港</span>
                </div>
                <div class="fallback-row">
                  <span class="arrow-icon">→</span>
                  <span>其他城市加入</span>
                  <span class="fallback-link">大湾区区域群</span>
                </div>
              </div>
            </div>

            <!-- 东北 -->
            <div class="region-block">
              <div class="region-header">
                <span class="region-name">东北</span>
                <span class="region-tag">区域群</span>
              </div>
              <div class="region-body">
                <p class="text-sm text-muted mb-3">沈阳、大连、长春等</p>
                <div class="fallback-row" style="border-top: none; margin-top: 0; padding-top: 0;">
                  <span class="arrow-icon">→</span>
                  <span>所有城市先加入</span>
                  <span class="fallback-link">东北区域群</span>
                </div>
              </div>
            </div>

            <!-- 川渝 -->
            <div class="region-block">
              <div class="region-header">
                <span class="region-name">川渝</span>
                <span class="region-tag">区域群</span>
              </div>
              <div class="region-body">
                <p class="text-sm text-muted mb-3">成都、重庆等</p>
                <div class="fallback-row" style="border-top: none; margin-top: 0; padding-top: 0;">
                  <span class="arrow-icon">→</span>
                  <span>所有城市先加入</span>
                  <span class="fallback-link">川渝区域群</span>
                  <span style="margin-left: auto; font-size: 12px; color: #c9a87c;">体量达标后开设城市群</span>
                </div>
              </div>
            </div>

            <!-- 更多省份 -->
            <div class="region-block">
              <div class="region-header">
                <span class="region-name">更多省份</span>
                <span class="region-tag">省级群</span>
              </div>
              <div class="region-body">
                <div class="flex flex-wrap gap-3">
                  <span class="city-pill"><span class="status-dot"></span>安徽</span>
                  <span class="city-pill"><span class="status-dot"></span>山东</span>
                  <span class="city-pill"><span class="status-dot"></span>新疆</span>
                  <span class="city-pill"><span class="status-dot"></span>河南</span>
                  <span class="city-pill"><span class="status-dot"></span>江西</span>
                </div>
              </div>
            </div>

          </div>
        </div>

      </div>
    </div>
  </section>

  <!-- 扫码加入 -->
  <section class="py-8 px-6">
    <div class="max-w-4xl mx-auto">

      <div class="bg-white border rounded-2xl p-8 md:p-10" style="border-color: #e8e4df;">

        <!-- 顶部说明 -->
        <div class="text-center mb-8">
          <h2 class="text-xl font-medium mb-2" style="color: #1a1a1a;">加入流程</h2>
          <p class="text-sm text-muted">三步完成，24小时内审核通过</p>
        </div>

        <!-- 三步流程 -->
        <div class="grid grid-cols-3 gap-4 mb-10">
          <div class="text-center">
            <div class="w-10 h-10 rounded-full flex items-center justify-center mx-auto mb-3" style="background: rgba(201,168,124,0.1);">
              <span class="text-accent text-sm font-bold">1</span>
            </div>
            <p class="text-sm font-medium mb-1" style="color: #1a1a1a;">扫码添加</p>
            <p class="text-xs text-muted">备注「城市+行业」</p>
          </div>
          <div class="text-center">
            <div class="w-10 h-10 rounded-full flex items-center justify-center mx-auto mb-3" style="background: rgba(201,168,124,0.1);">
              <span class="text-accent text-sm font-bold">2</span>
            </div>
            <p class="text-sm font-medium mb-1" style="color: #1a1a1a;">等待审核</p>
            <p class="text-xs text-muted">确认身份与属地</p>
          </div>
          <div class="text-center">
            <div class="w-10 h-10 rounded-full flex items-center justify-center mx-auto mb-3" style="background: rgba(201,168,124,0.1);">
              <span class="text-accent text-sm font-bold">3</span>
            </div>
            <p class="text-sm font-medium mb-1" style="color: #1a1a1a;">入群连接</p>
            <p class="text-xs text-muted">按属地分配社群</p>
          </div>
        </div>

        <!-- 分隔线 -->
        <div class="border-t mb-8" style="border-color: #e8e4df;"></div>

        <!-- 二维码 -->
        <div class="text-center">
          <p class="text-sm text-muted mb-6">添加微信，备注「城市 + 行业」</p>
          <div class="bg-white rounded-lg p-3 inline-block mb-4" style="border: 1px solid #e8e4df;">
            <img src="/assets/images/wechat-qr.jpg" alt="微信二维码" class="w-40 h-40 object-cover rounded">
          </div>
          <p class="text-sm font-medium mb-1" style="color: #1a1a1a;">24小时内拉你入群</p>
          <p class="text-xs text-muted">审核通过后，按属地分配对应社群</p>
        </div>

      </div>

      <p class="text-muted text-xs mt-6 text-center italic">让每一次连接，都创造真正价值</p>

    </div>
  </section>
  <!-- 社群公约 -->
  <section class="py-6 px-6">
    <div class="max-w-4xl mx-auto">
      <h2 class="section-title text-xl font-medium mb-4" style="color: #1a1a1a;">社群公约</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-3 mt-6">
        <div class="rule-card bg-white border rounded-lg p-4" style="border-color: #e8e4df;">
          <div class="flex items-start gap-4">
            <div class="w-8 h-8 rounded-full flex items-center justify-center shrink-0 mt-0.5" style="background: rgba(201,168,124,0.1);">
              <span style="color: #c9a87c;" class="text-xs font-medium">01</span>
            </div>
            <div>
              <h4 class="font-medium text-sm mb-1" style="color: #1a1a1a;">推文限额</h4>
              <p class="text-sm text-muted leading-relaxed">每人每周仅限分享一篇。好文一篇足矣，宁缺毋滥。</p>
            </div>
          </div>
        </div>
        <div class="rule-card bg-white border rounded-lg p-4" style="border-color: #e8e4df;">
          <div class="flex items-start gap-4">
            <div class="w-8 h-8 rounded-full flex items-center justify-center shrink-0 mt-0.5" style="background: rgba(201,168,124,0.1);">
              <span style="color: #c9a87c;" class="text-xs font-medium">02</span>
            </div>
            <div>
              <h4 class="font-medium text-sm mb-1" style="color: #1a1a1a;">AI内容</h4>
              <p class="text-sm text-muted leading-relaxed">禁止直接转发AI对话。请截取关键部分并附上你的解读。</p>
            </div>
          </div>
        </div>
        <div class="rule-card bg-white border rounded-lg p-4" style="border-color: #e8e4df;">
          <div class="flex items-start gap-4">
            <div class="w-8 h-8 rounded-full flex items-center justify-center shrink-0 mt-0.5" style="background: rgba(201,168,124,0.1);">
              <span style="color: #c9a87c;" class="text-xs font-medium">03</span>
            </div>
            <div>
              <h4 class="font-medium text-sm mb-1" style="color: #1a1a1a;">禁止霸屏</h4>
              <p class="text-sm text-muted leading-relaxed">请勿刷屏。各美其美，无需冗余；真知灼见，自会共鸣。</p>
            </div>
          </div>
        </div>
        <div class="rule-card bg-white border rounded-lg p-4" style="border-color: #e8e4df;">
          <div class="flex items-start gap-4">
            <div class="w-8 h-8 rounded-full flex items-center justify-center shrink-0 mt-0.5" style="background: rgba(201,168,124,0.1);">
              <span style="color: #c9a87c;" class="text-xs font-medium">04</span>
            </div>
            <div>
              <h4 class="font-medium text-sm mb-1" style="color: #1a1a1a;">产品推广</h4>
              <p class="text-sm text-muted leading-relaxed">允许自荐，每周一次。专注执行的你，不必重复推广。</p>
            </div>
          </div>
        </div>
        <div class="rule-card bg-white border rounded-lg p-4" style="border-color: #e8e4df;">
          <div class="flex items-start gap-4">
            <div class="w-8 h-8 rounded-full flex items-center justify-center shrink-0 mt-0.5" style="background: rgba(201,168,124,0.1);">
              <span style="color: #c9a87c;" class="text-xs font-medium">05</span>
            </div>
            <div>
              <h4 class="font-medium text-sm mb-1" style="color: #1a1a1a;">敏感话题</h4>
              <p class="text-sm text-muted leading-relaxed">涉及政治、宗教等敏感领域请谨慎发言，避免争议。</p>
            </div>
          </div>
        </div>
        <div class="rule-card bg-white border rounded-lg p-4" style="border-color: #e8e4df;">
          <div class="flex items-start gap-4">
            <div class="w-8 h-8 rounded-full flex items-center justify-center shrink-0 mt-0.5" style="background: rgba(201,168,124,0.1);">
              <span style="color: #c9a87c;" class="text-xs font-medium">06</span>
            </div>
            <div>
              <h4 class="font-medium text-sm mb-1" style="color: #1a1a1a;">尊重差异</h4>
              <p class="text-sm text-muted leading-relaxed">允许不同立场，反对无谓对立。理性探讨，对事不对人。</p>
            </div>
          </div>
        </div>
      </div>

      <div class="mt-4 bg-white border rounded-lg p-4 text-center" style="border-color: #e8e4df;">
        <p class="text-sm text-muted">
          <span class="font-medium" style="color: #1a1a1a;">违规处理：</span>首次提醒，二次移出。
        </p>
      </div>
    </div>
  </section>
  <!-- 属地规则 -->
  <section class="py-6 px-6">
    <div class="max-w-4xl mx-auto">
      <h2 class="section-title text-xl font-medium mb-4" style="color: #1a1a1a;">属地规则</h2>

      <div class="mt-6">
        <div class="bg-white border rounded-xl p-4 mb-4" style="border-color: #e8e4df;">
          <div class="flex items-center gap-3 mb-1">
            <div class="w-10 h-10 rounded-full flex items-center justify-center shrink-0" style="background: rgba(201,168,124,0.1);">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" style="color: #c9a87c;">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/>
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/>
              </svg>
            </div>
            <div>
              <p class="font-semibold text-base" style="color: #1a1a1a;">全国群仅限加入一个</p>
              <p class="text-xs text-muted">属地筛选 · 定期清理</p>
            </div>
          </div>
        </div>

        <div class="bg-white border rounded-xl p-4" style="border-color: #e8e4df;">
          <div class="rule-step">
            <div class="rule-step-num">1</div>
            <div>
              <p class="text-sm font-medium mb-1" style="color: #1a1a1a;">属地认定</p>
              <p class="text-sm text-muted leading-relaxed">区域群仅面向属地成员或明确计划落地OPC业务的创业者开放。不接受"观望"或"未来可能"等模糊状态。</p>
            </div>
          </div>
          <div class="rule-step">
            <div class="rule-step-num">2</div>
            <div>
              <p class="text-sm font-medium mb-1" style="color: #1a1a1a;">入群备注</p>
              <p class="text-sm text-muted leading-relaxed mb-2">入群后请修改备注：</p>
              <div class="rule-highlight">姓名/昵称-领域-所在区域</div>
              <p class="text-sm text-muted leading-relaxed mt-2">24小时内未修改者将收到提醒。</p>
            </div>
          </div>
          <div class="rule-step">
            <div class="rule-step-num">3</div>
            <div>
              <p class="text-sm font-medium mb-1" style="color: #1a1a1a;">清理机制</p>
              <p class="text-sm text-muted leading-relaxed">不符合属地条件的群友将被滚动请离。群内禁止无关广告、灌水及非属地城市的资源对接。</p>
              <div class="rule-warning">
                <p class="text-sm text-muted">违规即移，不另行通知。</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
  <!-- FAQ -->
  <section class="py-6 px-6 pb-20">
    <div class="max-w-4xl mx-auto">
      <h2 class="section-title text-xl font-medium mb-4" style="color: #1a1a1a;">常见问题</h2>

      <div class="mt-6 space-y-2 max-w-4xl">
        <div class="faq-item bg-white border rounded-lg overflow-hidden cursor-pointer" style="border-color: #e8e4df;" onclick="toggleFaq(this)">
          <div class="flex items-center justify-between p-5">
            <div class="flex items-center gap-3">
              <div class="w-6 h-6 rounded-full flex items-center justify-center shrink-0" style="background: rgba(201,168,124,0.1);">
                <span style="color: #c9a87c;" class="text-xs font-medium">Q</span>
              </div>
              <span class="text-sm font-medium" style="color: #1a1a1a;">可以同时加入多个群吗？</span>
            </div>
            <svg class="faq-icon w-4 h-4 text-muted transition-transform duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 4v16m8-8H4"/>
            </svg>
          </div>
          <div class="faq-content px-5">
            <p class="text-sm text-muted pb-5 leading-relaxed pl-9">全国群仅限加入一个。区域/省级群每人限加入一个对应属地的群，不支持同时存在于多个区域群。</p>
          </div>
        </div>

        <div class="faq-item bg-white border rounded-lg overflow-hidden cursor-pointer" style="border-color: #e8e4df;" onclick="toggleFaq(this)">
          <div class="flex items-center justify-between p-5">
            <div class="flex items-center gap-3">
              <div class="w-6 h-6 rounded-full flex items-center justify-center shrink-0" style="background: rgba(201,168,124,0.1);">
                <span style="color: #c9a87c;" class="text-xs font-medium">Q</span>
              </div>
              <span class="text-sm font-medium" style="color: #1a1a1a;">为什么需要审核？</span>
            </div>
            <svg class="faq-icon w-4 h-4 text-muted transition-transform duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 4v16m8-8H4"/>
            </svg>
          </div>
          <div class="faq-content px-5">
            <p class="text-sm text-muted pb-5 leading-relaxed pl-9">我们要交付信任的人。审核是为了确保每位成员都是真实的OPC创业者或从业者，维护社群质量。</p>
          </div>
        </div>

        <div class="faq-item bg-white border rounded-lg overflow-hidden cursor-pointer" style="border-color: #e8e4df;" onclick="toggleFaq(this)">
          <div class="flex items-center justify-between p-5">
            <div class="flex items-center gap-3">
              <div class="w-6 h-6 rounded-full flex items-center justify-center shrink-0" style="background: rgba(201,168,124,0.1);">
                <span style="color: #c9a87c;" class="text-xs font-medium">Q</span>
              </div>
              <span class="text-sm font-medium" style="color: #1a1a1a;">社群是免费的吗？</span>
            </div>
            <svg class="faq-icon w-4 h-4 text-muted transition-transform duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 4v16m8-8H4"/>
            </svg>
          </div>
          <div class="faq-content px-5">
            <p class="text-sm text-muted pb-5 leading-relaxed pl-9">是的，所有社群均为免费加入。我们依靠成员自发贡献与价值交换维持运营，而非会员费。</p>
          </div>
        </div>

        <div class="faq-item bg-white border rounded-lg overflow-hidden cursor-pointer" style="border-color: #e8e4df;" onclick="toggleFaq(this)">
          <div class="flex items-center justify-between p-5">
            <div class="flex items-center gap-3">
              <div class="w-6 h-6 rounded-full flex items-center justify-center shrink-0" style="background: rgba(201,168,124,0.1);">
                <span style="color: #c9a87c;" class="text-xs font-medium">Q</span>
              </div>
              <span class="text-sm font-medium" style="color: #1a1a1a;">我的城市没有专属群怎么办？</span>
            </div>
            <svg class="faq-icon w-4 h-4 text-muted transition-transform duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 4v16m8-8H4"/>
            </svg>
          </div>
          <div class="faq-content px-5">
            <p class="text-sm text-muted pb-5 leading-relaxed pl-9">可先加入所属区域群或全国总群。当所在城市成员达到一定规模时，我们会开设城市专属群。</p>
          </div>
        </div>
      </div>
    </div>
  </section>
</div>
<script>
  function toggleFaq(element) {
    const isActive = element.classList.contains('active');
    document.querySelectorAll('.community-page .faq-item').forEach(item => {
      item.classList.remove('active');
    });
    if (!isActive) {
      element.classList.add('active');
    }
  }
</script>