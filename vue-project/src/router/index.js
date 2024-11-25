import { createRouter, createWebHistory } from "vue-router";
import ArticleList from "@/components/ArticleList.vue";
import DetailView from "@/views/DetailView.vue";
import CreateView from "@/views/CreateView.vue";
import SignUpView from "@/views/SignUpView.vue";
import LogInView from "@/views/LogInView.vue";
import MovieView from "@/views/MovieView.vue";
import MovieDetail from "@/components/MovieDetail.vue";
import MyPageView from "@/views/MyPageView.vue";
import { useCounterStore } from "@/stores/counter";
import RegionSelectView from "@/views/RegionSelectView.vue";
import GenreSelectView from "@/views/GenreSelectView.vue";
import FilteredMoviesView from "@/views/FilteredMoviesView.vue";
import MovieReviewEditView from "@/views/MovieReviewEditView.vue";
import LatestMoviesView from "@/views/LatestMoviesView.vue";
import MainView from "@/views/MainView.vue";
import MovieRecommendView from "@/views/MovieRecommendView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "MainView",
      component: MainView,
    },
    {
      path: "/movies/recommend",
      name: "MovieRecommendView",
      component: MovieRecommendView,
    },
    {
      path: "/articles/:id",
      name: "DetailView",
      component: DetailView,
    },
    {
      path: "/create",
      name: "CreateView",
      component: CreateView,
    },
    {
      path: "/signup",
      name: "SignUpView",
      component: SignUpView,
    },
    {
      path: "/login",
      name: "LogInView",
      component: LogInView,
    },
    {
      path: "/movies",
      name: "MovieView",
      component: MovieView,
      meta: { requiresAuth: true },
    },
    {
      path: "/movies/:id",
      name: "MovieDetail",
      component: () => import("@/components/MovieDetail.vue"),
      props: true,
    },
    // component: MovieDetail,
    {
      path: "/mypage",
      name: "MyPageView",
      component: MyPageView,
    },
    {
      path: "/users/:username",
      name: "UserProfile",
      component: () => import("@/views/MyPageView.vue"),
      props: true,
    },
    {
      path: "/users/:username/profile",
      name: "UserProfile",
      component: MyPageView,
      props: true,
    },
    {
      path: "/articles",
      name: "ArticleList",
      component: ArticleList,
    },
    {
      path: "/article/:id/edit",
      name: "ArticleEditView",
      component: () => import("../views/ArticleEditView.vue"),
      meta: { requiresAuth: true },
    },

    {
      path: "/movies/:movieId/reviews/:reviewId/edit",
      name: "MovieReviewEditView",
      component: MovieReviewEditView,
      props: true,
    },
    {
      path: "/movies/select-region",
      name: "region-select",
      component: RegionSelectView,
      meta: { requiresAuth: true },
    },
    {
      path: "/movies/select-genre",
      name: "genre-select",
      component: GenreSelectView,
      meta: { requiresAuth: true },
    },
    {
      path: "/movies/filtered",
      name: "filtered-movies",
      component: FilteredMoviesView,
      meta: { requiresAuth: true },
    },
    {
      path: "/latest-movies",
      name: "LatestMoviesView",
      component: LatestMoviesView,
      meta: { requiresAuth: true }, // 로그인 필요 시 설정
    },
  ],
});

router.beforeEach((to, from, next) => {
  const counterStore = useCounterStore();

  if (to.meta.requiresAuth && !counterStore.isLogin) {
    window.alert("로그인이 필요합니다.");
    next({ name: "LogInView" });
    return;
  }

  // 이미 로그인된 경우 로그인/회원가입 페이지 접근 제한
  if (
    (to.name === "SignUpView" || to.name === "LogInView") &&
    counterStore.isLogin
  ) {
    window.alert("이미 로그인 되어있습니다.");
    next({ name: "MovieRecommendView" });
    return;
  }
  next();
});

export default router;
