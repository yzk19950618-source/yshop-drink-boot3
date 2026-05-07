package co.yixiang.yshop.server.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.web.configuration.WebSecurityCustomizer;

/**
 * classpath static 下商品缩略图等路径须匿名访问；仅靠 authorize permitAll 在部分环境下仍走认证入口，此处整体跳过 SecurityFilterChain。
 */
@Configuration
public class StaticResourceSecurityConfiguration {

    @Bean
    public WebSecurityCustomizer shopStaticResourcesCustomizer() {
        return web -> web.ignoring().requestMatchers("/shop-products/**");
    }
}
