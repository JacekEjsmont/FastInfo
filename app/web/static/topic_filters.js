(() => {
  const filterButtons = Array.from(document.querySelectorAll("[data-topic-filter]"));

  if (!filterButtons.length) return;

  const allButton = filterButtons.find((button) => button.dataset.topicFilter === "all") || null;
  const topicButtons = filterButtons.filter((button) => button !== allButton);

  function getActiveTopics() {
    return topicButtons
      .filter((button) => button.classList.contains("is-active"))
      .map((button) => button.dataset.topicFilter || "")
      .filter(Boolean);
  }

  function syncButtons() {
    const activeTopics = getActiveTopics();
    if (allButton) {
      const isAllActive = activeTopics.length === 0;
      allButton.classList.toggle("is-active", isAllActive);
      allButton.setAttribute("aria-pressed", String(isAllActive));
    }

    topicButtons.forEach((button) => {
      const isActive = button.classList.contains("is-active");
      button.setAttribute("aria-pressed", String(isActive));
    });
  }

  function syncEmptyStates() {
    document.querySelectorAll("[data-article-list]").forEach((list) => {
      const visibleRows = list.querySelectorAll("[data-article-row]:not(.is-hidden)").length;
      const empty = list.querySelector(".articles-empty");
      if (empty) {
        empty.hidden = visibleRows > 0;
      }
    });
  }

  function clusterMatchesTopics(clusterTopics, activeTopics) {
    if (activeTopics.size === 0) return true;
    if (!clusterTopics) return false;

    const topics = clusterTopics
      .split("|")
      .map((topic) => topic.trim())
      .filter(Boolean);

    return topics.some((topic) => activeTopics.has(topic));
  }

  function applyFilter() {
    const activeTopics = new Set(getActiveTopics());
    const shouldShowAll = activeTopics.size === 0;

    document.querySelectorAll("[data-info-cluster-row]").forEach((row) => {
      const clusterTopics = row.dataset.clusterTopics || "";
      const shouldShow = clusterMatchesTopics(clusterTopics, activeTopics);
      row.classList.toggle("is-hidden", !shouldShow);
    });

    document.querySelectorAll("[data-article-row]").forEach((row) => {
      const topic = (row.dataset.articleTopic || "").trim();
      const shouldShow = shouldShowAll || activeTopics.has(topic);
      row.classList.toggle("is-hidden", !shouldShow);
    });

    syncEmptyStates();
  }

  function clearAllTopics() {
    topicButtons.forEach((button) => button.classList.remove("is-active"));
    if (allButton) {
      allButton.classList.add("is-active");
    }
    syncButtons();
    applyFilter();
  }

  filterButtons.forEach((button) => {
    button.addEventListener("click", () => {
      const topic = button.dataset.topicFilter || "all";
      if (topic === "all") {
        clearAllTopics();
        return;
      }

      button.classList.toggle("is-active");
      if (allButton) {
        allButton.classList.remove("is-active");
      }

      const activeTopics = getActiveTopics();
      if (activeTopics.length === 0 && allButton) {
        allButton.classList.add("is-active");
      }

      syncButtons();
      applyFilter();
    });
  });

  document.addEventListener("htmx:afterSwap", applyFilter);
  document.addEventListener("DOMContentLoaded", applyFilter);
  syncButtons();
  applyFilter();
})();
