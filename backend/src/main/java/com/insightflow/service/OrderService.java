package com.insightflow.service;

import java.time.LocalDateTime;
import java.util.List;
import java.util.stream.Collectors;

import org.springframework.stereotype.Service;

import com.insightflow.dto.OrderDto;
import com.insightflow.mapper.OrderMapper;
import com.insightflow.model.Order;
import com.insightflow.repository.OrderRepository;

import lombok.RequiredArgsConstructor;

@Service
@RequiredArgsConstructor
public class OrderService {

    private final OrderRepository orderRepository;
    private final OrderMapper orderMapper;

    public List<OrderDto> findAll() {
        return orderRepository.findAll().stream()
                .map(orderMapper::toDto)
                .collect(Collectors.toList());
    }

    public OrderDto findById(Integer id) {
        Order order = orderRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Order not found with id: " + id));
        return orderMapper.toDto(order);
    }

    public List<OrderDto> findByUserId(Integer userId) {
        return orderRepository.findByUsersUserId(userId).stream()
                .map(orderMapper::toDto)
                .collect(Collectors.toList());
    }

    public List<OrderDto> findByStatus(String status) {
        return orderRepository.findByStatus(status).stream()
                .map(orderMapper::toDto)
                .collect(Collectors.toList());
    }

    public List<OrderDto> findByUserIdAndStatus(Integer userId, String status) {
        return orderRepository.findByUserIdAndStatus(userId, status).stream()
                .map(orderMapper::toDto)
                .collect(Collectors.toList());
    }

    public List<OrderDto> findByDateRange(LocalDateTime startDate, LocalDateTime endDate) {
        return orderRepository.findByOrderDateBetween(startDate, endDate).stream()
                .map(orderMapper::toDto)
                .collect(Collectors.toList());
    }

    public List<OrderDto> findUserOrdersOrderByDate(Integer userId) {
        return orderRepository.findByUserIdOrderByOrderDateDesc(userId).stream()
                .map(orderMapper::toDto)
                .collect(Collectors.toList());
    }

    public OrderDto create(OrderDto dto) {
        Order order = orderMapper.toEntity(dto);
        return orderMapper.toDto(orderRepository.save(order));
    }

    public OrderDto updateStatus(Integer id, String status) {
        Order order = orderRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Order not found with id: " + id));
        order.setStatus(status);
        return orderMapper.toDto(orderRepository.save(order));
    }

    public void delete(Integer id) {
        if (!orderRepository.existsById(id)) {
            throw new RuntimeException("Order not found with id: " + id);
        }
        orderRepository.deleteById(id);
    }
}
