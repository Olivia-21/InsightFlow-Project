package com.insightflow.service;

import java.util.List;
import java.util.stream.Collectors;

import com.insightflow.model.Users;
import org.springframework.stereotype.Service;

import lombok.RequiredArgsConstructor;
import com.insightflow.mapper.UserMapper;
import com.insightflow.repository.UserRepository;
import com.insightflow.dto.UserDto;

@Service
@RequiredArgsConstructor
public class UserService {

    private final UserRepository userRepository;
    private final UserMapper userMapper;

    public List<UserDto> findAll() {
        return userRepository.findAll().stream()
                .map(userMapper::toDto)
                .collect(Collectors.toList());
    }

    public UserDto findById(Integer id) {
        Users users = userRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("User not found with id: " + id));
        return userMapper.toDto(users);
    }

    public UserDto findByEmail(String email) {
        Users users = userRepository.findByEmail(email)
                .orElseThrow(() -> new RuntimeException("User not found with email: " + email));
        return userMapper.toDto(users);
    }

    public List<UserDto> findByRole(String role) {
        return userRepository.findByRole(role).stream()
                .map(userMapper::toDto)
                .collect(Collectors.toList());
    }

    public List<UserDto> searchByName(String name) {
        return userRepository.searchByName(name).stream()
                .map(userMapper::toDto)
                .collect(Collectors.toList());
    }

    public UserDto create(UserDto dto) {
        if (userRepository.existsByEmail(dto.getEmail())) {
            throw new RuntimeException("Email already registered: " + dto.getEmail());
        }
        Users users = userMapper.toEntity(dto);
        return userMapper.toDto(userRepository.save(users));
    }

    public UserDto update(Integer id, UserDto dto) {
        Users users = userRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("User not found with id: " + id));
        userMapper.updateEntityFromDto(dto, users);
        return userMapper.toDto(userRepository.save(users));
    }

    public void delete(Integer id) {
        if (!userRepository.existsById(id)) {
            throw new RuntimeException("User not found with id: " + id);
        }
        userRepository.deleteById(id);
    }

    public boolean existsByEmail(String email) {
        return userRepository.existsByEmail(email);
    }
}
