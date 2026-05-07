/**
 * Copyright (C) 2018-2022
 * All rights reserved, Designed By www.yixiang.co

 */
package co.yixiang.yshop.module.order.enums;

import lombok.AllArgsConstructor;
import lombok.Getter;

import java.util.stream.Stream;

/**
 * @author hupeng
 * 支付相关枚举
 */
@Getter
@AllArgsConstructor
public enum PayTypeEnum {

	CASH("cash","现金支付"),
	ALI("alipay","支付宝支付"),
	WEIXIN("weixin","微信支付"),
	/** 开发联调用：走 /order/pay 与微信相同的下单形态，服务端直接置已支付（需配置开启） */
	WEIXIN_MOCK("weixin_mock","模拟微信支付"),
	YUE("yue","余额支付"),
	INTEGRAL("integral","积分兑换");


	private String value;
	private String desc;

	public static PayTypeEnum toType(String value) {
		return Stream.of(PayTypeEnum.values())
				.filter(p -> p.value.equals(value))
				.findAny()
				.orElse(null);
	}


}
