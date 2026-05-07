package co.yixiang.yshop.server.config;

import org.redisson.spring.starter.RedissonAutoConfigurationCustomizer;
import org.springframework.boot.autoconfigure.AutoConfigureAfter;
import org.springframework.boot.autoconfigure.data.redis.RedisAutoConfiguration;
import org.springframework.boot.autoconfigure.data.redis.RedisProperties;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.util.StringUtils;

/**
 * 腾讯云等环境中占位符 / 空环境变量会使 Redis 密码变为空串，Redisson 仍会发 AUTH，
 * 免密实例返回 {@code ERR AUTH ... without any password configured}。
 * 在 Redisson 创建客户端前清空「空白密码」。
 */
@Configuration(proxyBeanMethods = false)
@AutoConfigureAfter(RedisAutoConfiguration.class)
public class YshopRedissonRedisFixConfiguration {

    @Bean
    public RedissonAutoConfigurationCustomizer yshopRedissonClearBlankPasswordCustomizer(RedisProperties redisProperties) {
        return config -> {
            if (StringUtils.hasText(redisProperties.getPassword())) {
                return;
            }
            if (config.isSingleConfig()) {
                config.useSingleServer().setPassword(null);
            } else if (config.isSentinelConfig()) {
                config.useSentinelServers().setPassword(null);
            } else if (config.isClusterConfig()) {
                config.useClusterServers().setPassword(null);
            }
        };
    }
}
