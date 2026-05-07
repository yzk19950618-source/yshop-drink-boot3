package co.yixiang.yshop.server.config;

import org.redisson.spring.starter.RedissonAutoConfigurationCustomizer;
import org.springframework.boot.autoconfigure.AutoConfigureAfter;
import org.springframework.boot.autoconfigure.data.redis.RedisAutoConfiguration;
import org.springframework.boot.autoconfigure.data.redis.RedisProperties;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.core.env.Environment;
import org.springframework.util.StringUtils;

/**
 * Redis/Redisson 云上适配：<br>
 * 1) 清空「空白密码」，避免免密实例仍发 AUTH。<br>
 * 2) 提高 Netty worker、TCP keep-alive、周期性 PING，减轻跨 VPC 链路 idle 断连后
 * Spring Data Redis Stream（XREADGROUP BLOCK）刷屏 {@code ClosedChannelException}。
 */
@Configuration(proxyBeanMethods = false)
@AutoConfigureAfter(RedisAutoConfiguration.class)
public class YshopRedissonRedisFixConfiguration {

    @Bean
    public RedissonAutoConfigurationCustomizer yshopRedissonCustomizer(RedisProperties redisProperties, Environment env) {
        return config -> {
            clearBlankPasswordIfNeeded(config, redisProperties);

            Integer nettyThreads = env.getProperty("yshop.cloud.redisson.netty-threads", Integer.class);
            if (nettyThreads != null && nettyThreads > 0) {
                config.setNettyThreads(nettyThreads);
            }

            Integer pingMs = env.getProperty("yshop.cloud.redisson.ping-connection-interval-ms", Integer.class);
            if (pingMs == null || pingMs <= 0) {
                return;
            }
            int ping = pingMs;
            if (config.isSingleConfig()) {
                config.useSingleServer().setPingConnectionInterval(ping).setKeepAlive(true);
            } else if (config.isSentinelConfig()) {
                config.useSentinelServers().setPingConnectionInterval(ping).setKeepAlive(true);
            } else if (config.isClusterConfig()) {
                config.useClusterServers().setPingConnectionInterval(ping).setKeepAlive(true);
            }
        };
    }

    private static void clearBlankPasswordIfNeeded(org.redisson.config.Config config, RedisProperties redisProperties) {
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
    }
}
