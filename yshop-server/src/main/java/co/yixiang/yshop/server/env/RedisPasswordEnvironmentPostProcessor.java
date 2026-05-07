package co.yixiang.yshop.server.env;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.env.EnvironmentPostProcessor;
import org.springframework.core.Ordered;
import org.springframework.core.env.ConfigurableEnvironment;
import org.springframework.core.env.MapPropertySource;
import org.springframework.util.StringUtils;

import java.util.Map;

/**
 * 仅当 {@code REDIS_PASSWORD} 非空时写入 {@code spring.data.redis.password}。
 * <p>避免 YAML 中 {@code password: ${REDIS_PASSWORD:}} 在无环境变量时变成空字符串，
 * Redisson 仍发 AUTH，而免密 Redis 返回 {@code ERR AUTH ... without any password configured}。
 */
public class RedisPasswordEnvironmentPostProcessor implements EnvironmentPostProcessor, Ordered {

    static final String PROPERTY_SOURCE_NAME = "yshopRedisPasswordFromEnv";

    @Override
    public int getOrder() {
        return Ordered.LOWEST_PRECEDENCE;
    }

    @Override
    public void postProcessEnvironment(ConfigurableEnvironment environment, SpringApplication application) {
        if (StringUtils.hasText(environment.getProperty("spring.data.redis.password"))) {
            return;
        }
        String redisPassword = environment.getProperty("REDIS_PASSWORD");
        if (!StringUtils.hasText(redisPassword)) {
            return;
        }
        environment.getPropertySources().addLast(
                new MapPropertySource(PROPERTY_SOURCE_NAME, Map.of("spring.data.redis.password", redisPassword)));
    }
}
